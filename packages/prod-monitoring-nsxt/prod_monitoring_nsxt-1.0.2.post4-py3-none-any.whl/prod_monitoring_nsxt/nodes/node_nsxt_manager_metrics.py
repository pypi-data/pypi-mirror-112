from library_nsxt.services import NSXTAPIClient
from proc_monitoring.nodes import NodeGatherer

_PROP_CONNECTION = "connections"
_PROP_CONNECTION_NSXT_API = "nsxt_api"
_PROP_CONNECTION_HOST = "host"
_PROP_CONNECTION_USER = "user"
_PROP_CONNECTION_PASS = "pass"
_PROP_DISPLAY_NAME = "display_name"

_NSXT_KEY = "nsxt-metrics"
_CONN_KEY = "sys-metrics"
_API_TIMEOUT = 30.0


class NodeNSXTManagerMetrics(NodeGatherer):
    """Specific NSX-T Manager monitoring node that gathers the required metrics from a Manager node."""

    def __init__(self, args):
        """
        Instantiates a new NSXT Manager monitoring node.

        :param args: The arguments for the node. Check documentation for more details.
        """
        api_host = args[_PROP_CONNECTION][_PROP_CONNECTION_NSXT_API][_PROP_CONNECTION_HOST]
        api_user = args[_PROP_CONNECTION][_PROP_CONNECTION_NSXT_API][_PROP_CONNECTION_USER]
        api_pass = args[_PROP_CONNECTION][_PROP_CONNECTION_NSXT_API][_PROP_CONNECTION_PASS]
        self.display_name = args[_PROP_DISPLAY_NAME]

        self._api = NSXTAPIClient(api_host, api_user, api_pass, _API_TIMEOUT)
        self.node_type = self._api.get_node_type(self.display_name)

        NodeGatherer.__init__(self, args, reset_on_error=True)

    def _gather_metrics(self):
        # Log the current step into the INFO log.
        self._logger.info("Gathering general metrics for NSX-T Manager node at [%s]..." % self.display_name)

        # Get the status of the nsxt system
        nsx_version = self._api.get_manager_node_status(self.display_name)["version"].split(".")
        main_version = ".".join(nsx_version[0:2])
        full_version = ".".join(nsx_version)
        self._queue_nsxt_data(_NSXT_KEY, "MgrSftVersion", {"MgrVersionNum": main_version}, {"MgrVersion": full_version})

        # Get the management and control cluster status
        cluster_status = self._api.get_manager_cluster_status()
        mng = 0 if cluster_status["mgmt_cluster_status"]["status"] == "STABLE" else 1
        ctrl = 0 if cluster_status["control_cluster_status"]["status"] == "STABLE" else 1
        self._queue_nsxt_data(_NSXT_KEY, "MgrCluster", {"MgrClusterStatus": mng, "CtrlClusterStatus": ctrl}),

        # Get the status of the specific manager
        manager_status = self._api.get_manager_node_status(self.display_name)["mgmt_cluster_status"]["mgmt_cluster_status"]
        manager_connected = 0 if manager_status == "CONNECTED" else 1
        self._queue_nsxt_data(_NSXT_KEY, "MgrConnected", {"MgrConnectedStatus": manager_connected})

        # Get the TX Bytes and RX Bytes for all interfaces of the node
        interfaces = self._api.get_manager_node_interfaces(self.display_name)
        interfaces_tx_rx = {itf["interface_id"]: (itf["statistics"]["tx_bytes"], itf["statistics"]["rx_bytes"]) for itf in interfaces}
        for itf, (tx, rx) in interfaces_tx_rx.items():
            self._queue_nsxt_data(_NSXT_KEY, "PhysicalPort", {"RxBytes": rx, "TxBytes": tx}, {"PhysicalPort": itf})

        # Get the status for all services deployed in the NSXT node
        services = self._api.get_manager_services(self.display_name)
        for srv in services:
            if srv["status"] == "running":
                srv["status"] = 0
            else:
                srv["status"] = 1
            self._queue_nsxt_data(_NSXT_KEY, "Services", {"ServiceState": srv["status"]}, {"Service": srv["service_name"]})

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