# Restaurant Kitchen Inventory App

A comprehensive, modular Streamlit application for managing restaurant inventory, recipes, variance calculations, and physical count management with real-time editing capabilities.

## 🚀 Features

### 📦 **Product Database Management**
- **Location-based organization** - Track products by storage locations
- **Price history tracking** - Monitor current and historical pricing
- **Bulk import/export** - CSV-based data management
- **Category management** - Organized product categorization
- **SKU tracking** - Unique product identification

### 📋 **Recipe Builder**
- **Ingredient management** - Add/remove ingredients with quantities
- **Cost calculations** - Automatic recipe cost analysis
- **Category organization** - Recipe categorization system
- **Portion scaling** - Adjust recipe quantities
- **Cost per unit tracking** - Detailed cost breakdown

### 📊 **Variance Calculator**
- **Expected vs Actual** - Compare planned vs actual usage
- **Cost variance analysis** - Financial impact calculations
- **Percentage tracking** - Variance percentage calculations
- **Detailed reporting** - Comprehensive variance reports

### 📋 **Sheet-to-Shelf Inventory**
- **Physical count management** - Conduct inventory counts
- **Location-based counting** - Sequential counting by location
- **Auto-save functionality** - Real-time count updates
- **Variance tracking** - Monitor count accuracy
- **Progress tracking** - Count completion status

### 📊 **Inventory Summary (NEW!)**
- **Editable count corrections** - Fix miscounts directly from summary
- **Location-based grouping** - Organized inventory analysis
- **Real-time calculations** - Auto-updating values and variances
- **Financial analysis** - Value calculations and cost tracking
- **Export functionality** - User-selectable download locations

### 💾 **Advanced Export Features**
- **User-selectable downloads** - Choose where to save CSV files
- **Detailed reporting** - Comprehensive data exports
- **Timestamped files** - Prevent file overwrites
- **Multiple export formats** - Count data and summary exports

## 🏗️ Project Structure

```
restuarnt_inventory_app/
├── app.py                    # Main Streamlit application
├── data/                     # Data storage (CSV, JSON, images)
│   ├── product_data.csv      # Product database
│   ├── recipes.json          # Recipe data
│   ├── inventory_counts.json # Active count data
│   └── count_history.json   # Historical count data
├── modules/                  # Business logic modules
│   ├── product_manager.py    # Product database management
│   ├── recipe_engine.py      # Recipe building and cost calculation
│   ├── variance_engine.py    # Variance analysis
│   ├── inventory_engine.py   # Physical count management
│   └── summary_engine.py     # Inventory summary and analysis
├── pages/                    # Streamlit UI pages
│   ├── 1_ProductDatabase.py  # Product management interface
│   ├── 2_RecipeBuilder.py    # Recipe creation and editing
│   ├── 3_VarianceCalculator.py # Variance analysis interface
│   ├── 4_SheetToShelfInventory.py # Physical count management
│   └── 5_InventorySummary.py # Editable summary and analysis
├── ui_components/            # Reusable UI components
│   ├── forms.py             # Form components
│   ├── layout.py            # Layout utilities
│   └── sidebar.py           # Navigation sidebar
├── utils/                    # Utility functions
│   ├── shared_functions.py  # Shared utility functions
│   └── error_handler.py     # Error handling utilities
├── tests/                    # Unit tests
└── requirements.txt          # Python dependencies
```

## 🚀 Quick Start

### **Installation**
```bash
# Clone the repository
git clone https://github.com/jkatz015/restaurant_inventory_app.git
cd restaurant_inventory_app

# Install dependencies
pip install -r requirements.txt
```

### **Running the App**
```bash
# Start the Streamlit application
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### **Running Tests**
```bash
# Run all unit tests
python -m unittest discover tests
```

## 📖 Usage Guide

### **1. Product Database Setup**
1. Navigate to "📦 Product Database"
2. Add products with locations, categories, and pricing
3. Use bulk import for large product lists
4. Track price history and updates

### **2. Recipe Management**
1. Go to "📋 Recipe Builder"
2. Create recipes with ingredients and quantities
3. View automatic cost calculations
4. Organize recipes by categories

### **3. Variance Analysis**
1. Access "📊 Variance Calculator"
2. Compare expected vs actual usage
3. Analyze cost variances and percentages
4. Generate detailed variance reports

### **4. Physical Inventory Counting**
1. Navigate to "📋 Sheet-to-Shelf Inventory"
2. Start a new count with location filtering
3. Count items sequentially by location
4. Auto-save functionality updates in real-time
5. Complete counts and move to history

### **5. Inventory Summary & Corrections**
1. Go to "📊 Inventory Summary"
2. View comprehensive count summaries by location
3. **Edit actual counts directly** - Fix miscounts without returning to counting page
4. Download detailed CSV reports to your chosen location
5. Analyze financial impact and variance trends

## 🆕 Latest Features

### **Editable Summary Page**
- **Direct count corrections** - Edit actual counts from summary view
- **Real-time calculations** - Values and variances update automatically
- **Location-based organization** - Grouped by storage locations
- **Visual variance indicators** - Color-coded variance tracking

### **User-Selectable Downloads**
- **Choose download location** - Save CSV files where you want
- **Standard browser experience** - Native download dialogs
- **Timestamped filenames** - Prevent file overwrites
- **Multiple export types** - Count data and summary exports

### **Enhanced Inventory Management**
- **Location-based counting** - Sequential inventory by storage area
- **Auto-save functionality** - Real-time count updates
- **Progress tracking** - Monitor count completion status
- **Variance analysis** - Comprehensive accuracy reporting

## 🛠️ Technical Features

- **Modular Architecture** - Separated UI, business logic, and data layers
- **Multi-language Support** - English and Spanish interfaces
- **Real-time Updates** - Auto-save and live calculations
- **Error Handling** - Comprehensive error management
- **Data Validation** - Input validation and data integrity
- **Export Capabilities** - Multiple export formats and locations
- **Responsive Design** - Works on desktop and mobile devices

## 🧪 Testing

The application includes comprehensive unit tests for all major modules:

```bash
# Run specific test modules
python -m unittest tests.test_products
python -m unittest tests.test_recipes
python -m unittest tests.test_inventory
python -m unittest tests.test_variance

# Run all tests with coverage
python -m unittest discover tests -v
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Add tests** for new functionality
4. **Commit changes** (`git commit -m 'Add amazing feature'`)
5. **Push to branch** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

### **Development Guidelines**
- Add business logic to `modules/`
- Add UI components to `ui_components/`
- Add new pages to `pages/`
- Use shared functions from `utils/shared_functions.py`
- Include tests for new features
- Follow existing code patterns and naming conventions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation above

---

**Built with ❤️ using Streamlit, Pandas, and Python** 