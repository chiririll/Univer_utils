import subprocess


def export_emf(src: str):
    subprocess.call(f'D:\\Program Files\\Inkscape\\bin\\inkscape.exe --export-type="emf" {src}')
