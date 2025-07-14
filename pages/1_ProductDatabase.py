import streamlit as st
import pandas as pd
from modules.product_manager import (
    get_text, initialize_product_data, load_products, save_product, 
    delete_product, update_product, bulk_update_prices, format_currency, 
    format_currency_small, UNIT_CONVERSIONS, calculate_cost_per_oz
)

def main():
    """Product Database page - Manage product catalog and inventory items"""
    
    # Language toggle
    lang = st.radio("Language", ["English", "Spanish"], horizontal=True)
    current_lang = "es" if lang == "Spanish" else "en"
    
    st.header(get_text("page_title", current_lang))
    st.markdown(get_text("page_caption", current_lang))
    
    # Initialize product data
    init_result = initialize_product_data()
    if init_result:
        st.success(init_result)
    
    # Load existing products
    products_df = load_products()
    
    # Create tabs for different functions
    tab1, tab2, tab3, tab4 = st.tabs([
        get_text("product_list", current_lang),
        get_text("add_new_product", current_lang), 
        get_text("manage_products", current_lang),
        get_text("bulk_update_title", current_lang)
    ])
    
    # Tab 1: Product List
    with tab1:
        st.subheader(get_text("product_list", current_lang))
        
        if products_df.empty:
            st.info(get_text("no_products_found", current_lang))
        else:
            # Search functionality
            search_term = st.text_input(get_text("search_products", current_lang))
            
            # Filter by category and location
            col1, col2 = st.columns(2)
            
            with col1:
                categories = ["All Categories"] + sorted(products_df['Category'].dropna().unique().tolist())
                selected_category = st.selectbox(get_text("filter_by_category", current_lang), categories)
            
            with col2:
                locations = ["All Locations"] + sorted(products_df['Location'].dropna().unique().tolist())
                selected_location = st.selectbox("Filter by Location", locations)
            
            # Filter products
            filtered_df = products_df.copy()
            
            if search_term:
                mask = (filtered_df['Product Name'].str.contains(search_term, case=False, na=False) |
                       filtered_df['SKU'].str.contains(search_term, case=False, na=False))
                filtered_df = filtered_df[mask]
            
            if selected_category != "All Categories":
                filtered_df = filtered_df[filtered_df['Category'] == selected_category]
            
            if selected_location != "All Locations":
                filtered_df = filtered_df[filtered_df['Location'] == selected_location]
            
            # Display results
            st.write(get_text("showing_products", current_lang, 
                            filtered=len(filtered_df), 
                            total=len(products_df)))
            
            if len(filtered_df) == 0:
                st.info(get_text("no_products_match", current_lang))
            else:
                # Format currency columns
                display_df = filtered_df.copy()
                
                # Format last price with proper null handling
                def format_last_price(x):
                    import pandas as pd
                    if pd.notna(x) and x != '' and x is not None:
                        return format_currency(x)
                    return '-'
                
                def format_last_date(x):
                    import pandas as pd
                    if pd.notna(x) and x != '' and x is not None:
                        return str(x)
                    return '-'
                
                # Apply formatting to each column - using list comprehension to avoid linter issues
                try:
                    import pandas as pd
                    
                    # Format current price
                    current_prices = [format_currency(x) for x in display_df['Current Price per Unit']]
                    display_df['Current Price per Unit'] = current_prices
                    
                    # Format last price with null handling
                    last_prices = []
                    for x in display_df['Last Price per Unit']:
                        if pd.notna(x) and x != '' and x is not None:
                            last_prices.append(format_currency(x))
                        else:
                            last_prices.append('-')
                    display_df['Last Price per Unit'] = last_prices
                    
                    # Format last updated date
                    last_dates = []
                    for x in display_df['Last Updated Date']:
                        if pd.notna(x) and x != '' and x is not None:
                            last_dates.append(str(x))
                        else:
                            last_dates.append('-')
                    display_df['Last Updated Date'] = last_dates
                    
                    # Format cost per oz
                    cost_per_oz_values = [format_currency_small(x) for x in display_df['Cost per Oz']]
                    display_df['Cost per Oz'] = cost_per_oz_values
                    
                except Exception as e:
                    st.error(f"Error formatting display data: {e}")
                
                st.dataframe(display_df, use_container_width=True)
            
            # Summary statistics
            st.subheader(get_text("summary", current_lang))
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(get_text("total_products", current_lang), len(products_df))
            
            with col2:
                if not products_df.empty:
                    most_expensive = products_df.loc[products_df['Current Price per Unit'].idxmax()]
                    st.metric(get_text("most_expensive", current_lang), 
                             most_expensive['Product Name'],
                             format_currency(most_expensive['Current Price per Unit']))
                else:
                    st.metric(get_text("most_expensive", current_lang), get_text("na", current_lang))
            
            with col3:
                if not products_df.empty:
                    total_value = products_df['Current Price per Unit'].sum()
                    st.metric(get_text("total_inventory_value", current_lang), 
                             format_currency(total_value))
                else:
                    st.metric(get_text("total_inventory_value", current_lang), get_text("na", current_lang))
            
            with col4:
                if not products_df.empty:
                    top_category = products_df['Category'].value_counts().index[0] if not products_df['Category'].empty else get_text("na", current_lang)
                    count = products_df['Category'].value_counts().iloc[0] if not products_df['Category'].empty else 0
                    st.metric(get_text("top_category", current_lang), 
                             str(top_category),
                             f"{count} {get_text('items', current_lang)}")
                else:
                    st.metric(get_text("top_category", current_lang), get_text("na", current_lang))
    
    # Tab 2: Add New Product
    with tab2:
        st.subheader(get_text("add_new_product", current_lang))
        
        with st.form("add_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                product_name = st.text_input(get_text("product_name", current_lang))
                sku = st.text_input(get_text("sku", current_lang))
                location_options = ["Walk-in Cooler", "Dry Goods Storage", "Freezer"]
                location = st.selectbox(get_text("location", current_lang), location_options, help=get_text("location_help", current_lang))
                category = st.text_input(get_text("category", current_lang))
                pack_size = st.text_input(get_text("pack_size", current_lang))
            
            with col2:
                unit_options = ["oz", "lb", "case", "each", "gallon", "liter", "quart", "grams"]
                unit = st.selectbox(get_text("unit_of_measure", current_lang), unit_options)
                cost_per_unit = st.number_input(
                    get_text("cost_per_unit", current_lang),
                    min_value=0.0,
                    step=0.01,
                    help=get_text("cost_per_unit_help", current_lang)
                )
            
            # Show cost per ounce preview
            if cost_per_unit > 0 and unit:
                conversion = UNIT_CONVERSIONS.get(unit.lower(), 1)
                cost_per_oz = calculate_cost_per_oz(cost_per_unit, unit)
                st.info(get_text("cost_per_ounce_preview", current_lang, 
                               cost=format_currency_small(cost_per_oz), 
                               unit=unit, 
                               conversion=conversion))
            
            submitted = st.form_submit_button(get_text("add_product_button", current_lang))
            
            if submitted:
                if not product_name:
                    st.error(get_text("please_enter_name", current_lang))
                else:
                    product = {
                        'name': product_name,
                        'sku': sku,
                        'location': location,
                        'category': category,
                        'pack_size': pack_size,
                        'unit': unit,
                        'cost': cost_per_unit
                    }
                    
                    success, message = save_product(product)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    

    
    # Tab 3: Manage Products
    with tab3:
        st.subheader(get_text("manage_products", current_lang))
        
        if products_df.empty:
            st.info(get_text("no_products_found", current_lang))
        else:
            # Delete Product
            st.write("### " + get_text("delete_a_product", current_lang))
            product_to_delete = st.selectbox(get_text("select_product_delete", current_lang), 
                                           products_df['Product Name'].tolist())
            
            if st.button(get_text("delete_button", current_lang)):
                if product_to_delete:
                    success, message = delete_product(product_to_delete)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning(get_text("select_product_delete_warning", current_lang))
            
            st.divider()
            
            # Edit Product
            st.write("### " + get_text("edit_a_product", current_lang))
            product_to_edit = st.selectbox(get_text("select_product_edit", current_lang), 
                                         products_df['Product Name'].tolist())
            
            if product_to_edit:
                product_row = products_df[products_df['Product Name'] == product_to_edit].iloc[0]
                st.write(get_text("editing", current_lang, name=product_to_edit))
                
                with st.form("edit_product_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input(get_text("product_name", current_lang), value=product_row['Product Name'])
                        new_sku = st.text_input(get_text("sku", current_lang), value=product_row['SKU'])
                        new_category = st.text_input(get_text("category", current_lang), value=product_row['Category'])
                        new_pack_size = st.text_input(get_text("pack_size", current_lang), value=product_row['Pack Size'])
                    
                    with col2:
                        location_options = ["Walk-in Cooler", "Dry Goods Storage", "Freezer"]
                        current_location = product_row.get('Location', 'Dry Goods Storage')
                        new_location = st.selectbox(get_text("location", current_lang), location_options, 
                                                  index=location_options.index(current_location) if current_location in location_options else 1,
                                                  help=get_text("location_help", current_lang))
                        unit_options = ["oz", "lb", "case", "each", "gallon", "liter", "quart", "grams"]
                        new_unit = st.selectbox(get_text("unit_of_measure", current_lang), 
                                              unit_options, 
                                              index=unit_options.index(product_row['Unit']) if product_row['Unit'] in unit_options else 0)
                        new_cost = st.number_input(get_text("cost_per_unit", current_lang), 
                                                 value=float(product_row['Current Price per Unit']), 
                                                 min_value=0.0, 
                                                 step=0.01)
                    
                    submitted = st.form_submit_button(get_text("update_product_button", current_lang))
                    
                    if submitted:
                        updated_product = {
                            'name': new_name,
                            'sku': new_sku,
                            'location': new_location,
                            'category': new_category,
                            'pack_size': new_pack_size,
                            'unit': new_unit,
                            'cost': new_cost
                        }
                        
                        success, message = update_product(product_to_edit, updated_product)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
    
    # Tab 4: Bulk Update from Supplier CSV
    with tab4:
        st.subheader(get_text("bulk_update_title", current_lang))
        
        uploaded_file = st.file_uploader(get_text("upload_supplier_csv", current_lang), type=['csv'])
        
        if uploaded_file is not None:
            try:
                import pandas as pd
                supplier_df = pd.read_csv(uploaded_file)
                
                st.write("### " + get_text("supplier_csv_preview", current_lang))
                st.dataframe(supplier_df.head(), use_container_width=True)
                
                st.write("### " + get_text("column_mapping", current_lang))
                col1, col2 = st.columns(2)
                
                with col1:
                    sku_column = st.selectbox(get_text("select_sku_column", current_lang), supplier_df.columns.tolist())
                
                with col2:
                    price_column = st.selectbox(get_text("select_price_column", current_lang), supplier_df.columns.tolist())
                
                if st.button(get_text("update_prices_button", current_lang)):
                    if sku_column and price_column:
                        success, message = bulk_update_prices(supplier_df, sku_column, price_column)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Please select both SKU and Price columns.")
                        
            except Exception as e:
                st.error(f"Error reading CSV file: {e}")

if __name__ == "__main__":
    main()