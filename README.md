
# 📚 Book Recommendation System

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-plastic&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-plastic&logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/ML-FF6F00?style=for-plastic&logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-plastic&logo=pandas&logoColor=white)

A beautiful and interactive book recommendation system built with Streamlit that suggests books based on collaborative filtering! 🌟

## ✨ Features

- 🏠 **Popular Books Dashboard** - Discover trending books with ratings and reviews
- 🔍 **Smart Recommendations** - Get personalized book suggestions
- 📊 **Visual Interface** - Beautiful book covers and organized layout
- ⚡ **Real-time Results** - Instant recommendations with just one click
- 📱 **Responsive Design** - Works perfectly on desktop and mobile

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/subhadipsinha722133/Book-Recommender-System.git
   cd book-recommendation-system
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Place your data files** in the project directory:
   - `popular.pkl`
   - `pt.pkl`
   - `books.pkl`
   - `similarity_scores.pkl`

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** and go to `http://localhost:8501`

## 🎯 How to Use

1. **Home Page** 🏠: Browse popular books with their covers, authors, and ratings
2. **Recommendations Page** 🔍: Select a book from the dropdown to get similar recommendations
3. **Explore** 🔎: Click through different books and discover new reading options!

## 🛠️ Technologies Used

- **Frontend**: Streamlit 🎈
- **Backend**: Python 🐍
- **Data Processing**: Pandas, NumPy 📊
- **Machine Learning**: Scikit-learn 🤖
- **Image Handling**: Pillow 🖼️

## 📁 Project Structure

```
book-recommendation-system/
├── main_app.py                 # 🎯 Main Streamlit application
├── requirements.txt       # 📦 Python dependencies
├── README.md             # 📖 This file
├── popular.pkl           # 📊 Popular books data
├── pt.pkl               # 🔢 Pivot table data
├── books.pkl            # 📚 Books metadata
└── similarity_scores.pkl # 💫 Precomputed similarity scores
```

## 🎨 Customization

Want to customize this app? Here's what you can modify:

- **Colors & Theme**: Edit Streamlit configuration in `app.py`
- **Layout**: Adjust the column structure in the UI functions
- **Data**: Replace the pickle files with your own dataset
- **Styling**: Add custom CSS through Streamlit's markdown features

## 🤝 Contributing

Want to contribute? Awesome! 🎉

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

**Subhadip Sinha** 👨‍💻  
- GitHub: [@subhadipsinha722133](https://github.com/subhadipsinha722133)  
- Email: sinhasubhadip34@gmail.com  

## 🙏 Acknowledgments

- Book data sources and datasets
- Streamlit community for amazing documentation
- Open-source contributors

---

⭐ **If you like this project, give it a star on GitHub!** ⭐

Made with ❤️ by Subhadip Sinha

This README includes:

1. **Your personal details** with username `subhadipsinha722133`
2. **Lots of emojis** throughout the document (📚✨🚀🎯🛠️ etc.)
3. **Comprehensive sections** covering all aspects of the project
4. **Badges** for technologies used
5. **Clear installation instructions**
6. **Visual structure** with proper formatting
7. **Customization guide** for future modifications
8. **Contact information** section

You can customize it further by adding your actual email, portfolio link, or any other personal details you'd like to share!
