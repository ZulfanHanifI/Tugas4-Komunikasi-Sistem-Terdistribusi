# RPC Server (XML-RPC, modul bawaan Python, tanpa instalasi library)
from xmlrpc.server import SimpleXMLRPCServer

HOST = "0.0.0.0"   # 0.0.0.0 wajib di container agar bisa diakses dari luar container
PORT = 8000
BATAS_MAKS = 1_000_000  # pengaman agar server tidak hang


def rpc_prima(n):
    """Mengembalikan list bilangan prima dari 2 sampai n. Contoh: rpc_prima(11) -> [2, 3, 5, 7, 11]"""
    n = int(n)
    if n < 2:
        return []
    if n > BATAS_MAKS:
        raise ValueError(f"Batas maksimum {BATAS_MAKS}")
    # Sieve of Eratosthenes
    prima = [True] * (n + 1)
    prima[0] = prima[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if prima[i]:
            for j in range(i * i, n + 1, i):
                prima[j] = False
    return [i for i, p in enumerate(prima) if p]


def main():
    server = SimpleXMLRPCServer((HOST, PORT), allow_none=True, logRequests=True)
    server.register_function(rpc_prima, "rpc_prima")
    print(f"[V] RPC Server berjalan di {HOST}:{PORT}", flush=True)
    print("[i] Service tersedia: rpc_prima(n). Tekan Ctrl+C untuk keluar.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server dihentikan.")


if __name__ == "__main__":
    main()
