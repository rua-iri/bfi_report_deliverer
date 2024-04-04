# bfi_report_deliverer

## Installation

### Clone the repository

```bash 
git clone https://github.com/rua-iri/bfi_report_deliverer

cd bfi_report_deliverer
```


### Create virtual environment and install requirements

```bash
python3 -m venv venv

pip3 install -r requirements.txt
```

### Create .env file with the following variables

```bash
touch .env
```

```yaml
RESEND_API_KEY=<API_KEY>

FROM_EMAIL=<EMAIL_ADDRESS>
```


### Run program

```bash 
python3 main.py
```

