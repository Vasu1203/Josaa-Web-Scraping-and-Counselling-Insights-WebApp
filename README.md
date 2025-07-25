# 🎓 JoSAA Counselling Insights WebApp

This project is a combination of **web scraping and data visualization** to help students explore **JoSAA counselling data** in an interactive and insightful way.  

Using **Python and Selenium**, the latest **Seat Matrix (2025)** and **Opening & Closing Ranks (OR–CR 2024)** were scraped from the official **JoSAA website**. A modern **Streamlit web application** was then developed to help students explore colleges based on their rank, view **NIRF rankings**, and analyze seat availability.

---

## 🕸️ Data Collection (Web Scraping)

- **Tools Used:** `Selenium`, `BeautifulSoup`, `pandas`  
- **Source Website:** [https://josaa.nic.in](https://josaa.nic.in)  
- **Scraped Data:**
  - 🎯 **Opening and Closing Ranks (2024)** for all participating institutes  
  - 🪑 **Seat Matrix (2025)** including gender-neutral, female-only, and supernumerary categories  

- Data was cleaned and exported into CSV files for efficient analysis and dashboard integration.

---

## 📊 WebApp Features (Streamlit)

The dashboard was built using **Streamlit** and includes:

- 🔢 **Rank-Based College Explorer:**  
  - Enter your rank, category, gender, and round to view eligible colleges and branches  
- 🏛️ **NIRF Ranking Integration:**  
  - View NIRF ranks of institutions directly in your search results  
- 📈 **Seat Matrix Visualizer:**  
  - View detailed seat matrix of institutes by category, gender, and branch  
- 🔍 **Search & Filter Options:**  
  - Filter by branch, quota, or institute type for customized exploration  
- 💡 **User-Friendly Interface:**  
  - Built with responsiveness and simplicity using Streamlit widgets and layout options  

---

## 📦 Technologies Used

**Backend / Scraping: Python, Selenium, BeautifulSoup**

**Frontend / Dashboard: Streamlit**

**Data Handling: pandas, numpy**

**Others: NIRF data integration**

 ## Key Benefits

**🔍 Accurate college predictions based on live data**

**📈 Insightful seat availability and ranking info**

**🧠 Useful for both students and counselors during JoSAA rounds**

## ⚙️ How to Run Locally

#### 1. Clone the Repository
**git clone https://github.com/Vasu1203/Josaa-Web-Scraping-and-Counselling-Insights-WebApp.git**

#### 2. Create virtual environment
python -m venv venv

#### 3. Activate on Windows
venv\Scripts\activate

#### 4. Activate on macOS/Linux
source venv/bin/activate

#### 5. Install Dependencies
pip install -r requirements.txt

#### 6. Run the Streamlit App
streamlit run app.py


