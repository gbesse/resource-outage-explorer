import json
from pathlib import Path
import sys

from .engine import analyze,verify_certificate

ROOT=Path(__file__).resolve().parent
MESSAGES={"fr":{"help":"Utilisation : python -m outage_explorer demo|analyze scénario.json|verify scénario.json certificat.json|serve [port] [--lang fr|en|es]","error":"Entrée non valide","ready":"Laboratoire de capacité local"},"en":{"help":"Usage: python -m outage_explorer demo|analyze scenario.json|verify scenario.json certificate.json|serve [port] [--lang fr|en|es]","error":"Invalid input","ready":"Local capacity laboratory"},"es":{"help":"Uso: python -m outage_explorer demo|analyze escenario.json|verify escenario.json certificado.json|serve [puerto] [--lang fr|en|es]","error":"Entrada no válida","ready":"Laboratorio de capacidad local"}}


def example():return json.loads((ROOT/"examples/shared-depot.json").read_text())


def main(argv=None):
    args=list(sys.argv[1:] if argv is None else argv);lang="en"
    try:
        if "--lang" in args:
            i=args.index("--lang");lang=args[i+1];del args[i:i+2]
        if lang not in MESSAGES:raise ValueError("invalid_language")
        if not args or args[0] in ("help","--help"):print(MESSAGES[lang]["help"]);return 0
        command=args.pop(0)
        if command=="demo":result=analyze(example())
        elif command=="analyze" and len(args)==1:result=analyze(json.loads(Path(args[0]).read_text()))
        elif command=="verify" and len(args)==2:result=verify_certificate(json.loads(Path(args[0]).read_text()),json.loads(Path(args[1]).read_text()))
        elif command=="serve":
            from .server import serve
            port=int(args[0]) if args else 8770;print(f'{MESSAGES[lang]["ready"]}: http://127.0.0.1:{port}/?lang={lang}',flush=True);serve(port);return 0
        else:raise ValueError("invalid_command")
        print(json.dumps(result,ensure_ascii=False,indent=2));return 1 if result.get("valid") is False else 0
    except (ValueError,TypeError,KeyError,IndexError,OSError):
        print(json.dumps({"error":"invalid_input","message":MESSAGES.get(lang,MESSAGES["en"])["error"]}),file=sys.stderr);return 2


if __name__=="__main__":raise SystemExit(main())
