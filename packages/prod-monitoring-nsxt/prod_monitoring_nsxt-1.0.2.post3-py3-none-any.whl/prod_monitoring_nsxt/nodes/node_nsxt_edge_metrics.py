from library_nsxt.services import NSXTAPIClient
from proc_monitoring.nodes import NodeGatherer

_PROP_CONNECTION = "connections"
_PROP_CONNECTION_NSXT_API = "nsxt_api"
_PROP_CONNECTION_HOST = "host"
_PROP_CONNECTION_USER = "user"
_PROP_CONNECTION_PASS = "pass"
_PROP_DISPLAY_NAME = "display_name"

_NSXT_KEY = "nsxt-metrics"
_UPDATE_NODE_PEERS_LIMIT = 20
_API_TIMEOUT = 30.0


class NodeNSXTEdgeMetrics(NodeGatherer):
    """Specific NSX-T Edge monitoring node that gathers the required metrics from an edge node."""

    def __init__(self, args):
        """
        Instantiates a new NSXT Edge monitoring node.

        :param args: The arguments for the node. Check documentation for more details.
        """
        api_host = args[_PROP_CONNECTION][_PROP_CONNECTION_NSXT_API][_PROP_CONNECTION_HOST]
        api_user = args[_PROP_CONNECTION][_PROP_CONNECTION_NSXT_API][_PROP_CONNECTION_USER]
        api_pass = args[_PROP_CONNECTION][_PROP_CONNECTION_NSXT_API][_PROP_CONNECTION_PASS]
        self.display_name = args[_PROP_DISPLAY_NAME]

        self._api = NSXTAPIClient(api_host, api_user, api_pass, _API_TIMEOUT)
        self.node_type = self._api.get_node_type(self.display_name)

        self.__node_tunnel_ips = None
        self.__update_node_peers_counter = _UPDATE_NODE_PEERS_LIMIT

        NodeGatherer.__init__(self, args, reset_on_error=True)

    def _gather_metrics(self):
        # Log the current step into the INFO log.
        self._logger.info("Gathering general metrics for NSX-T Edge node at [%s]..." % self.display_name)

        # Update the node peers if limit is hit
        if self.__update_node_peers_counter >= _UPDATE_NODE_PEERS_LIMIT:
            self._logger.info("Limit reached, updating node peers...")
            # self.__update_node_peers()
            self.__update_node_peers_counter = 0
            self._logger.info("Node peers updated...")

        # Get the edge node status
        transport_node_id = self._api.get_transport_node_uuid(self.display_name)
        srt0 = self._api.get_tier0_logical_router(self.display_name)

        for transport_node in srt0["per_node_status"]:
            if transport_node["transport_node_id"] == transport_node_id:
                edge_active = 0 if transport_node["high_availability_status"] == "ACTIVE" else 1

        cluster_status = 0 if srt0["edge_cluster_status"] == "UP" else 1
        self._queue_nsxt_data(_NSXT_KEY, "EdgeClusterStatus",
                            {"AdminState": cluster_status, "ActiveState": edge_active})

        # Check if there is a manager active
        manager_connection_status = self._api.get_transport_node_status(self.display_name)["mgmt_connection_status"]
        manager_connected = 0 if manager_connection_status == "UP" else 1
        self._queue_nsxt_data(_NSXT_KEY, "ManagerConn", {"MgrConnected": manager_connected})

        # Check if there is a controller active
        controller_connection_status = self._api.get_transport_node_status(self.display_name)["control_connection_status"]["status"]
        controller_connected = 0 if controller_connection_status == "UP" else 1
        self._queue_nsxt_data(_NSXT_KEY, "CtrlConn", {"CtrlConnected": controller_connected})

        if edge_active == 0:
            # Get the load balancer data
            for lb in self._api.get_load_balancers():
                if lb["enabled"]:
                    data = {
                        "LoadBalancerPoolNum": lb["lb_status"]["pool_num"],
                        "LoadBalancerPoolUpNum": lb["lb_status"]["pool_num_up"],
                        "LoadBalancerVsNum": lb["lb_status"]["vs_num"],
                        "LoadBalancerVsUpNum": lb["lb_status"]["vs_num_up"]
                    }
                    self._queue_nsxt_data(_NSXT_KEY, "LoadBalancerStatus", data,
                                        {"LoadBalancerName": lb["display_name"]})

                    for vs in lb["lb_status"]["virtual_servers"]:
                        tags = {
                            "LoadBalancerName": lb["display_name"],
                            "LoadBalancerVsDisplayName": vs["display_name"],
                            "LoadBalancerVsIpAddress": vs["ip_address"],
                            "LoadBalancerVsPort": vs["port"]
                        }
                        data = {
                            "LoadBalancerVsCurrSess": vs["statistics"]["current_sessions"],
                            "LoadBalancerVsSessRate": vs["statistics"]["current_session_rate"],
                            "LoadBalancerVsTotalSess": vs["statistics"]["total_sessions"],
                            "LoadBalancerVsRxBytes": vs["statistics"]["bytes_in"],
                            "LoadBalancerVsTxBytes": vs["statistics"]["bytes_out"]
                        }
                        self._queue_nsxt_data(_NSXT_KEY, "LoadBalancerVs", data, tags)

                    for pool in lb["lb_status"]["pools"]:
                        tags = {
                            "LoadBalancerName": lb["display_name"],
                            "LoadBalancerPoolDisplayName": pool["display_name"],
                        }
                        data = {
                            "LoadBalancerPoolCurrSess": pool["statistics"]["current_sessions"],
                            "LoadBalancerPoolSessRate": pool["statistics"]["current_session_rate"],
                            "LoadBalancerPoolTotalSess": pool["statistics"]["total_sessions"],
                            "LoadBalancerPoolRxBytes": pool["statistics"]["bytes_in"],
                            "LoadBalancerPoolTxBytes": pool["statistics"]["bytes_out"]
                        }
                        self._queue_nsxt_data(_NSXT_KEY, "LoadBalancerPool", data, tags)

                        for member in pool["members"]:
                            tags = {
                                "LoadBalancerName": lb["display_name"],
                                "LoadBalancerPoolDisplayName": pool["display_name"],
                                "LoadBalancerPoolMemberName": member["display_name"],
                            }
                            data = {
                                "LoadBalancerPoolMemberCurrSess": member["statistics"]["current_sessions"],
                                "LoadBalancerPoolMemberSessRate": member["statistics"]["current_session_rate"],
                                "LoadBalancerPoolMemberTotalSess": member["statistics"]["total_sessions"],
                                "LoadBalancerPoolMemberRxBytes": member["statistics"]["bytes_in"],
                                "LoadBalancerPoolMemberTxBytes": member["statistics"]["bytes_in"]

                            }
                            self._queue_nsxt_data(_NSXT_KEY, "LoadBalancerPool", data, tags)

    def _queue_nsxt_data(self, key, metric, data, tags=None):
        """
        Method that adds the metric to the message queue in the expected format with the expected metadata.

        :param str key: The key of the message, to group the messages according to type of data gathered.
        :param str metric: The main metric tag of the message. The specific type of data being gathered.
        :param dict[str, str or int or float] data: Data to be sent in the message.
        :param dict[str, str] or None tags: Optional additional tags that should be added to the message.
        """
        message_tags = tags if tags is not None else {}
        message_tags.update({
            "host": self.display_name,
            "infratype": self.node_type,
            "metric": metric
        })
        self._queue_data(key, message_tags, data)

    def __update_node_peers(self):
        """Updates the edge node tunnel peers."""
        transport_node_id = self._api.get_transport_node_uuid(self.display_name)
        self.__node_tunnel_peers = self._api.get_node_peers(transport_node_id)
