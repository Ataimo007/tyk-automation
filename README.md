# API Automation Tool

A Python automation tool for provisioning and deleting APIs via the Tyk Dashboard API.

---

## 📁 Project Structure

```
automation/
│
├── api/
│   ├── __init__.py
│   └── oas_bulk_jwt_manager.py   # API creation & product logic
│
├── config/
│   ├── __init__.py
│   └── settings.py               # Environment configuration loader
│
├── main.py                       # CLI entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment variables
└── .gitignore
```

---

## ⚙️ Requirements

- Python 3.9+
- Access to Tyk Dashboard
- Dashboard Admin API Key
- Organisation ID

---

## 🚀 Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd automation
```

---

### 2️⃣ Create Virtual Environment

Mac / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Then update:

```
DASHBOARD_URL=http://localhost:3000
API_KEY=your-dashboard-admin-api-key
ORG_ID=your-organisation-id
```

### Variable Reference

| Variable | Description |
|-----------|-------------|
| `DASHBOARD_URL` | Base URL of the Tyk Dashboard |
| `API_KEY` | Dashboard Admin API key with API management permissions |
| `ORG_ID` | Organisation ID from the Dashboard |

⚠️ Never commit your `.env` file.

---

## 🛠 Usage

### Create APIs

```bash
python main.py \
  --api-name demo \
  --number 2 \
  --jwks-uri https://example.com/jwks.json
```

---

### Create APIs With product Payload

```bash
python main.py \
  --api-name demo \
  --number 20 \
  --jwks-uri https://example.com/jwks.json \
  --product-payload \
  --provider-id 123 \
  --templates User
```

---

### Delete APIs

```bash
python main.py --api-name demo --delete
```

This deletes APIs matching the provided name prefix.

---

<!-- ## 🔐 Security Notes

- Do NOT commit `.env`
- Do NOT commit API keys
- Rotate keys if exposed -->