# Restaurant Kitchen Inventory App

A modular, multi-language Streamlit app for managing restaurant inventory, recipes, and variance calculations.

## Project Structure

```
restuarnt_inventory_app/
  app.py                  # Main entry point
  config.py               # Centralized configuration
  data/                   # Data files (CSV, JSON, images)
  modules/                # Business logic (product, recipe, inventory, variance)
  pages/                  # Streamlit UI pages
  tests/                  # Unit tests
  ui_components/          # Reusable UI components (forms, layout, sidebar)
  utils/                  # Utilities (file_loader, validator, error_handler)
  requirements.txt        # Python dependencies
  README.md               # This file
```

## Usage

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Run the app:**
   ```sh
   streamlit run app.py
   ```
3. **Run tests:**
   ```sh
   python -m unittest discover tests
   ```

## Key Features
- Modular codebase: UI, business logic, and data are separated
- Multi-language support (English, Spanish)
- Reusable UI components for forms, layout, and sidebar
- Centralized configuration and error handling
- Unit tests for all major modules

## Best Practices
- Add new business logic to `modules/`
- Add new UI elements to `ui_components/`
- Add new pages to `pages/`
- Use `utils/validator.py` for data validation
- Use `utils/file_loader.py` for file operations
- Use `config.py` for global settings
- Add tests for new features in `tests/`

## Contributing
Pull requests are welcome! Please add tests for new features and keep code modular. 