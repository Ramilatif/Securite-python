from src.tp1.utils.lib import choose_interface
from tp1.utils.config import logger
from scapy.all import *


class Capture:
    def __init__(self) -> None:
        self.interface = choose_interface()
        self.packets = []
        self.summary = ""

    def capture_traffic(self) -> None:
        """
        Capture network traffic from an interface
        """
        self.packets = sniff(iface=self.interface, count=20)
        logger.info(f"Capture traffic from interface {self.interface}")

    def sort_network_protocols(self) -> str:
        """
        Sort and return all captured network protocols by frequency (descending)
        """
        protocols: dict[str, int] = {}
        for pkt in self.packets:
            proto = pkt.lastlayer().name
            protocols[proto] = protocols.get(proto, 0) + 1
        sorted_protocols = sorted(protocols.items(), key=lambda x: x[1], reverse=True)
        return str(dict(sorted_protocols))

    def get_all_protocols(self) -> str:
        """
        Return all protocols captured with total packets number
        """
        protocols: dict[str, int] = {}
        for pkt in self.packets:
            for layer_class in pkt.layers():
                proto = layer_class.__name__
                protocols[proto] = protocols.get(proto, 0) + 1
        return str(protocols)

    def analyse(self, protocols: str) -> None:
        """
        Analyse all captured data and return statement.
        Si un trafic est illégitime (exemple : ARP Spoofing) :
          a. Noter la tentative d'attaque.
          b. Relever le protocole ainsi que l'adresse réseau/physique de l'attaquant.
        Sinon afficher que tout va bien.
        """
        all_protocols = self.get_all_protocols()
        sort = self.sort_network_protocols()
        logger.debug(f"All protocols: {all_protocols}")
        logger.debug(f"Sorted protocols: {sort}")

        # Détection ARP Spoofing
        arp_table: dict[str, str] = {}
        attacks_detected = False
        for pkt in self.packets:
            if ARP in pkt and pkt[ARP].op == 2:  # ARP reply
                ip = pkt[ARP].psrc
                mac = pkt[ARP].hwsrc
                if ip in arp_table and arp_table[ip] != mac:
                    logger.warning(
                        f"ARP Spoofing détecté ! "
                        f"Protocole : ARP | IP : {ip} | "
                        f"MAC attaquant : {mac} (précédent : {arp_table[ip]})"
                    )
                    attacks_detected = True
                else:
                    arp_table[ip] = mac

        if not attacks_detected:
            logger.info("Tout va bien : aucune activité suspecte détectée.")

        self.summary = self._gen_summary()

    def get_summary(self) -> str:
        """
        Return summary
        :return:
        """
        return self.summary

    def _gen_summary(self) -> str:
        """
        Generate summary
        """
        total = len(self.packets)
        protocols_str = self.get_all_protocols()
        sorted_str = self.sort_network_protocols()
        summary = (
            f"Résumé de la capture réseau\n"
            f"============================\n"
            f"Total paquets capturés : {total}\n"
            f"Protocoles détectés : {protocols_str}\n"
            f"Protocoles triés par fréquence : {sorted_str}\n"
        )
        return summary
