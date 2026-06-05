from scapy.all import get_if_list


def hello_world() -> str:
    """
    Hello world function

    :return: "hello world"
    """
    return "hello world"


def choose_interface() -> str:
    """
    Return network interface and input user choice

    :return: network interface
    """
    interfaces = get_if_list()
    if not interfaces:
        return ""

    print("Interfaces réseau disponibles :")
    for i, iface in enumerate(interfaces):
        print(f"  {i} - {iface}")

    while True:
        try:
            choice = input("Choisissez une interface (numéro) : ")
            idx = int(choice)
            if 0 <= idx < len(interfaces):
                return interfaces[idx]
            print(f"Veuillez entrer un nombre entre 0 et {len(interfaces) - 1}")
        except ValueError:
            print("Veuillez entrer un nombre valide")
        except (KeyboardInterrupt, EOFError):
            return ""
