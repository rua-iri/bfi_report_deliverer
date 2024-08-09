# bfi_report_deliverer

<div align="center">
  <div>
    A Python program to generate and deliver weekly reports about UK cinema
    </div>
  <br/>
  <div>
<img src="https://github.com/rua-iri/bfi_report_deliverer/assets/117874491/27e832fb-1c99-45eb-a190-04f88758c4cf" alt=bfi_report_deliverer logo" width="45%" />
    </div>
</div>



## Installation

### Clone the repository
```bash 
git clone https://github.com/rua-iri/bfi_report_deliverer

cd bfi_report_deliverer
```


### Create virtual environment and install requirements

```bash
python3 -m venv .venv

source .venv/bin/activate

pip3 install -r requirements.txt

sudo apt install wkhtmltopdf
```

### Create .env file with the following variables
```bash
touch .env
```

```yaml
ENV=staging

RESEND_API_KEY=<API_KEY>

FROM_EMAIL=<EMAIL_ADDRESS>

TMBD_API_KEY=<API_KEY>
```


### Run Setup
```
make setup
```

### Run program

```bash 
python3 main.py
```

### Run tests

```bash
make test
```


