"""Simple Windows 10 VM launcher using QEMU.

This does not include Windows itself. Provide your own legally obtained
Windows 10 ISO when launching the VM.
"""

from pathlib import Path
import argparse
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description="Launch a Windows 10 QEMU VM")
    parser.add_argument("--iso", required=True, help="Path to your Windows 10 ISO")
    parser.add_argument("--disk", default="windows10.qcow2", help="Virtual disk path")
    parser.add_argument("--ram", default="4G", help="RAM, e.g. 4G")
    parser.add_argument("--cpus", default="2", help="Number of virtual CPUs")
    args = parser.parse_args()

    qemu = shutil.which("qemu-system-x86_64")
    qemu_img = shutil.which("qemu-img")
    if not qemu or not qemu_img:
        raise SystemExit("Install QEMU and make qemu-system-x86_64 and qemu-img available in PATH.")

    iso = Path(args.iso).expanduser().resolve()
    disk = Path(args.disk).expanduser().resolve()
    if not iso.is_file():
        raise SystemExit(f"Windows 10 ISO not found: {iso}")

    if not disk.exists():
        print(f"Creating 64 GB virtual disk: {disk}")
        subprocess.run([qemu_img, "create", "-f", "qcow2", str(disk), "64G"], check=True)

    cmd = [
        qemu,
        "-machine", "q35,accel=tcg",
        "-m", args.ram,
        "-smp", args.cpus,
        "-drive", f"file={disk},format=qcow2",
        "-cdrom", str(iso),
        "-boot", "order=d,menu=on",
        "-vga", "std",
        "-nic", "user,model=e1000",
    ]
    print("Starting Windows 10 VM...")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
