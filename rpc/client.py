# RPC Client: memanggil rpc_prima() yang ada di server
import os
import sys
import time
import xmlrpc.client

HOST = os.environ.get("RPC_HOST", "localhost")
PORT = int(os.environ.get("RPC_PORT", "8000"))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    proxy = xmlrpc.client.ServerProxy(f"http://{HOST}:{PORT}/")
    print(f"[*] Memanggil rpc_prima({n}) ke {HOST}:{PORT} ...", flush=True)
    # retry: server di container kadang belum siap saat client dijalankan
    for percobaan in range(1, 11):
        try:
            hasil = proxy.rpc_prima(n)
            break
        except OSError:
            print(f"[!] Server belum siap (percobaan {percobaan}/10), coba lagi...", flush=True)
            time.sleep(1)
    else:
        print("[X] Gagal terhubung ke server.")
        sys.exit(1)
    print(f"[V] Hasil rpc_prima({n}) = {', '.join(map(str, hasil))}", flush=True)


if __name__ == "__main__":
    main()
