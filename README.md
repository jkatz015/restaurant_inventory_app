# 🍽️ Restaurant Kitchen Inventory

A comprehensive Streamlit-based application for managing restaurant inventory, tracking usage patterns, analyzing sales data, and optimizing stock levels. Built for **Curated Restaurant Consulting**.

## ✨ Features

- **📦 Product Database** - Manage product catalog with CRUD operations
- **👨‍🍳 Recipe Builder** - Create and manage recipes with ingredient lists
- **📊 Variance Calculator** - Calculate and analyze inventory variances
- **📋 Sheet-to-Shelf Inventory** - Conduct physical inventory counts
- **🎨 Professional UI** - Clean, mobile-friendly interface
- **🏢 Branded** - Curated Restaurant Consulting branding

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Windows (tested on Windows 10/11)

### Installation

1. **Clone or download** the repository
2. **Navigate** to the project directory:
   ```bash
   cd restuarnt_inventory_app
   ```

3. **Install dependencies**:
   ```bash
   py -m pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   py -m streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📁 Project Structure

```
restuarnt_inventory_app/
├── app.py                          # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── test_app.py                     # Test suite
├── README.md                       # This file
├── data/                           # Data files directory
│   ├── product_data.csv           # Product database
│   └── Curated Restaurant Consulting Logo for Business Card.png
├── pages/                          # Application pages
│   ├── 1_ProductDatabase.py       # Product management
│   ├── 2_RecipeBuilder.py         # Recipe creation
│   ├── 3_VarianceCalculator.py    # Variance analysis
│   └── 4_SheetToShelfInventory.py # Inventory counting
├── modules/                        # Core modules (future)
├── ui_components/                  # UI components (future)
├── utils/                          # Utility functions (future)
└── tests/                          # Test files (future)
```

## 🛠️ Usage

### Product Database
- **Add products** with name, category, unit, and cost
- **Search and filter** products by name or category
- **Edit and delete** existing products
- **View summary statistics**

### Recipe Builder
- Create recipes with ingredient lists
- Calculate recipe costs
- Manage recipe categories

### Variance Calculator
- Upload expected vs actual inventory data
- Calculate variance percentages
- Analyze cost impact
- Generate variance reports

### Sheet-to-Shelf Inventory
- Conduct physical inventory counts
- Track count accuracy
- Compare with expected levels

## 🧪 Testing

Run the test suite to verify everything works:

```bash
py test_app.py
```

This will test:
- ✅ Package imports
- ✅ Page module loading
- ✅ Data directory structure
- ✅ Logo file availability

## 📦 Dependencies

- **streamlit** >= 1.28.0 - Web application framework
- **pandas** >= 2.0.0 - Data manipulation
- **numpy** >= 1.24.0 - Numerical computing
- **plotly** >= 5.15.0 - Interactive charts
- **Pillow** >= 10.0.0 - Image processing
- **openpyxl** >= 3.1.0 - Excel file support
- **xlrd** >= 2.0.0 - Excel file reading
- **pytest** >= 7.0.0 - Testing framework

## 🎨 Customization

### Logo
Replace `data/Curated Restaurant Consulting Logo for Business Card.png` with your logo.

### Branding
Update the company name in `app.py`:
```python
st.markdown("**Curated Restaurant Consulting**")
```

### Colors and Styling
Modify the CSS in `app.py` to customize the appearance.

## 🔧 Development

### Adding New Pages
1. Create a new file in `pages/` directory
2. Include a `main()` function
3. Add navigation in `app.py`

### Adding Features
- Product database: Edit `pages/1_ProductDatabase.py`
- Recipe builder: Edit `pages/2_RecipeBuilder.py`
- Variance calculator: Edit `pages/3_VarianceCalculator.py`
- Inventory counting: Edit `pages/4_SheetToShelfInventory.py`

## 🐛 Troubleshooting

### Common Issues

**"Logo file not found"**
- Ensure logo file exists in `data/` directory
- Check file name spelling

**"Module not found"**
- Run `py -m pip install -r requirements.txt`
- Check Python version (3.7+)

**"Page not loading"**
- Ensure page has `main()` function
- Check file naming convention

### Getting Help
1. Run `py test_app.py` to diagnose issues
2. Check the console for error messages
3. Verify all dependencies are installed

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support with Curated Restaurant Consulting implementations, contact your consultant.

---

**Built with ❤️ for restaurant inventory management** 