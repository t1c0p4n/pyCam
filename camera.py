import cv2
import argparse
import time
import os
from datetime import datetime

def create_output_dir():
    dirname = "capturas"
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname

def capture_photo(qty_per_second: int, duration_minutes: int):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        return

    output_dir = create_output_dir()

    if duration_minutes == 0:
        # Captura única
        ret, frame = cam.read()
        if ret:
            filename = os.path.join(output_dir, f"foto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Foto salva: {filename}")
        cam.release()
        return

    # Captura múltipla
    total_seconds = duration_minutes * 60
    interval = 1 / qty_per_second
    end_time = time.time() + total_seconds

    print(f"Iniciando captura de {qty_per_second} fotos/s por {duration_minutes} minutos...")

    while time.time() < end_time:
        ret, frame = cam.read()
        if ret:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = os.path.join(output_dir, f"foto_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
        time.sleep(interval)

    cam.release()
    print("Captura de fotos encerrada.")

def capture_video(duration_minutes: int):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        return

    output_dir = create_output_dir()

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    filename = os.path.join(output_dir, f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi")
    fps = 20.0

    ret, frame = cam.read()
    if not ret:
        print("Erro ao ler a câmera.")
        cam.release()
        return

    height, width, _ = frame.shape
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

    total_seconds = duration_minutes * 60
    end_time = time.time() + total_seconds if duration_minutes > 0 else None

    print(f"Iniciando gravação de vídeo por {duration_minutes} minutos...")

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        out.write(frame)

        if end_time and time.time() >= end_time:
            break

    cam.release()
    out.release()
    print(f"Vídeo salvo: {filename}")
    print("Gravação encerrada.")

def main():
    parser = argparse.ArgumentParser(description="Captura de vídeo e fotos pela webcam")

    parser.add_argument("-v", action="store_true", help="Gravar vídeo")
    parser.add_argument("-f", action="store_true", help="Capturar foto")
    parser.add_argument("-q", type=int, default=1, help="Quantidade de fotos por segundo (1-100)")
    parser.add_argument("-t", type=int, default=0, help="Tempo em minutos (opcional)")

    args = parser.parse_args()

    # Validações
    if args.v and args.f:
        print("Erro: use apenas -v ou -f, não ambos ao mesmo tempo.")
        return

    if not args.v and not args.f:
        print("Erro: você deve escolher -v para vídeo ou -f para fotos.")
        return

    if args.f:
        if args.q < 1 or args.q > 100:
            print("Erro: o parâmetro -q deve estar entre 1 e 100.")
            return
        capture_photo(args.q, args.t)

    elif args.v:
        capture_video(args.t)

if __name__ == "__main__":
    main()

