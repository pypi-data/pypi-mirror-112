import io
import json
import dpkt

class Capture(object):

    def __init__(self, trexclient):
        self._client = trexclient
        self._captures = {}
        self._capture_states = {}
        self._cache = {}
        self._port_ids = []


    def set_port_ids(self, port_ids):
        self._port_ids = port_ids


    def set_capture(self, payload, port_ids):
        self._state = payload
        self._port_ids = port_ids
        cs = json.loads(payload.serialize())
        ports = list(range(len(port_ids)))
        if cs['port_names'] is not None and len(cs['port_names']) > 0:
            ports = []
            for p_name in cs['port_names']:
                ports.append(port_ids.index(p_name))

        if cs['state'] == 'start':
            for p in ports:
                self._captures[p] = self._client.start_capture(rx_ports = [p])
                if p in self._cache:
                    self._cache.pop(p)
                self._capture_states[p] = cs['state']
        elif cs['state'] == 'stop':
            for p in ports:
                if p in self._captures:
                    print('stop '+p)
                    self._cache[p] = []
                    self._client.fetch_capture_packets(self._captures[p]['id'], self._cache[p])
                    self._client.stop_capture(self._captures[p]['id'])
                    self._captures.pop(p)
                self._capture_states[p] = cs['state']

    def get_capture(self, request):
        port_idx = self._port_ids.index(request.port_name)
        res = io.BytesIO()
        wr = dpkt.pcap.Writer(res)

        pkt_list = []
        if port_idx in self._captures:
            self._client.fetch_capture_packets(self._captures[port_idx]['id'], pkt_list)
        elif port_idx in self._cache:
            pkt_list = self._cache.pop(port_idx)

        for pkt in pkt_list:
            wr.writepkt(pkt=pkt['binary'], ts=pkt['ts'])

        res.seek(0)
        return res

    def is_started(self, port_id):
        return port_id in self._capture_states and self._capture_states[port_id] == 'start'