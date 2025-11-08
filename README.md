# stripe_data_transformer
A Python tool that fetches Stripe data, transforms it, and exports clean CSV reports for analytics, finance, and bookkeeping workflows.



Here is a clean, practical **step-by-step action plan** you can follow to build your entire Stripe CSV Fetcher project.
✅ It’s structured so you can track progress and stay accountable.
✅ You can tick the boxes as you complete each task.

---

# ✅ **Stripe CSV Tool – Action Plan**

## ✅ **PHASE 1 — Project Setup**

* [x] **Create the project folder** (`stripe_csv_tool/`)
* [x] **Create subfolders**:

  * [x] `services/`
  * [ ] `utils/`
* [x] **Create required files**:

  * [ ] `main.py`
  * [ ] `config.py`
  * [ ] `requirements.txt`
* [x] **Install dependencies** (`pandas`, `requests`)

  ```bash
  pip install requests pandas
  ```

---

## ✅ **PHASE 2 — Config & Logging Setup**

* [ ] **Create `config.py`**

  * [x] Add `STRIPE_API_KEY`
  * [x] Add `CHARGES_URL = "https://api.stripe.com/v1/charges"`
  * [x] Add other endpoints if needed
  * ✅ *YES, it is fully okay to import from config inside your services.*

* [ ] **Set up logging (recommended location: `main.py`)**

  * [ ] Configure root logger (format, level)
  * [ ] Optionally write logs to a file `logs/app.log`
  * [ ] Import `logging` in service files and use `logging.getLogger(__name__)`

**Why logging in main?**
Because `main.py` is the entry point → it ensures ALL modules inherit the logging config automatically.

---

## ✅ **PHASE 3 — Write Services (Core Logic)**

### ✅ **1. `services/fetch_charges.py`**

* [x] Import `requests` and config values
* [x] Add a function `fetch_all_charges(api_key)`
* [x] Inside:

  * [x] Implement pagination
  * [x] Use `while has_more:`
  * [x] Append results to a list
  * [x] Return the list of charges
* [x] Add logging statements for debugging

  * e.g. “Fetched page 1: 100 charges”

### ✅ **2. (Optional) `services/fetch_customers.py`**

* [ ] Write function to fetch all customers with pagination
* [ ] Return a mapping `{customer_id: email}`
* [ ] Log count of customers fetched

### ✅ **3. (Optional) `services/fetch_refunds.py`**

* [ ] Same pattern as above
* [ ] Return list of refunds or mapping by charge ID

---

## ✅ **PHASE 4 — Data Transformation**

### ✅ **`services/transformer.py`**

* [ ] Import pandas + `json_normalize`

* [ ] Write function `charges_to_dataframe(charges)`

  * [ ] Flatten Stripe JSON
  * [ ] Inspect df columns
  * [ ] Select only the columns you want
  * [ ] Rename the columns
  * [ ] Convert timestamps
  * [ ] Convert amount from cents to dollars
  * [ ] Return cleaned DataFrame

* [ ] Write function `save_csv(df, filename="charges.csv")`

  * [ ] Export to CSV
  * [ ] Log "CSV saved successfully"

---

## ✅ **PHASE 5 — Connect Everything in `main.py`**

* [ ] Import services:

  * `fetch_all_charges`
  * `charges_to_dataframe`
  * `save_csv`

* [ ] Write your `run()` function:

  * [ ] Fetch all charges
  * [ ] Transform into DataFrame
  * [ ] Save CSV
  * [ ] Print success message
  * [ ] Log all steps

* [ ] Add entry-point guard:

  ```python
  if __name__ == "__main__":
      run()
  ```

---

## ✅ **PHASE 6 — Testing and Review**

* [ ] Run the tool in **test mode** using your test API key
* [ ] Confirm CSV output is correct
* [ ] Check logs to ensure no errors
* [ ] Add error-handling for:

  * [ ] Network failures
  * [ ] API auth failures
  * [ ] Empty results
  * [ ] Pagination issues

---

## ✅ **PHASE 7 — Deployment / Version 2**

(Do this once version 1 works)

* [ ] Add Customers and map emails into the charges DataFrame
* [ ] Add Refunds and link refunded amounts
* [ ] Make CLI flags (e.g., `--from-date`, `--to-date`)
* [ ] Add save to Excel option
* [ ] Optionally make a small API or CLI tool

---

# ✅ **BONUS: Where to start coding?**

Start in this order:

1. `config.py`
2. Logging in `main.py`
3. `fetch_charges.py`
4. `transformer.py`
5. Connect everything in `main.py`
6. Run the program
7. Improve it step by step

---

If you want, I can also generate a **code skeleton** for all files so you can fill them in one by one.
