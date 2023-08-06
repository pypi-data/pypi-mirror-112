r"""This module implementes Visa Derived Unique Key Per Transaction scheme.
In DUKPT each device is initialized with a distinct key derived from
a single key, the base derivation key (BDK).
A key derived from the BDK is known as the Initial PIN Encryption Key (IPEK).
IPEK is then injected into the devices.

Glossary:
- BDK - Base Derivation Key
- IPEK - Initial PIN Encryption Key

Atalla:
Derivation Key (DK)
A key which encrypts the Initial Key Serial Number (IKSN)
to obtain the Initial PIN Encryption Key (IPEK).

Key Serial Number (KSN)
A 20 character value that is transmitted from the EFT/POS
terminal to the host. It allows the host to determine the
key which encrypts the PIN. The KSN consists of the Initial
Key Serial Number (59 bits) + the Encryption Counter (21 bits).

Initial Key Serial Number (IKSN)
The leftmost 64 bits of the Key Serial Number.

Initial PIN Encryption Key (IPEK)
The result of encrypting the IKSN with the DK. (This value
does not encrypt a PIN); see Current PIN Encryption Key.

Current Key
The result of encryption of the KSN with the IPEK.

Current PIN Encryption Key
Exclusive-OR the last byte of current key with FF.

Current MAC Key (Visa)
Exclusive-OR the last two bytes of current key with FFFF.

DUKPT PIN
DUKPT MAC
"""
