import streamlit as st
from modules.recipe_engine import (
    get_text, load_products, load_recipes, save_recipe, update_recipe, 
    delete_recipe, get_recipe_categories, filter_recipes_by_category, 
    search_recipes, format_currency
)

def main():
    """Recipe Builder page - Create and manage recipes with ingredient lists"""
    
    # Language toggle
    lang = st.radio("Language", ["English", "Spanish"], horizontal=True)
    current_lang = "es" if lang == "Spanish" else "en"
    
    st.header(get_text("page_title", current_lang))
    st.markdown(get_text("page_caption", current_lang))
    
    # Load data
    products_df = load_products()
    recipes = load_recipes()
    
    # Create tabs for different functions
    tab1, tab2, tab3 = st.tabs([get_text("create_recipe", current_lang), get_text("view_recipes", current_lang), get_text("edit_recipe", current_lang)])
    
    # Tab 1: Create Recipe
    with tab1:
        st.subheader(get_text("create_new_recipe", current_lang))
        
        # Initialize ingredients list
        if "ingredients" not in st.session_state:
            st.session_state.ingredients = []
        
        # Ingredients management outside of form
        st.write("### " + get_text("ingredients", current_lang))
        
        if products_df.empty:
            st.warning("No products available. Please add products first.")
        else:
            # Display existing ingredients
            for i, ingredient in enumerate(st.session_state.ingredients):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    product_name = st.selectbox(
                        get_text("product", current_lang),
                        products_df['Product Name'].tolist(),
                        key=f"product_{i}",
                        index=products_df['Product Name'].tolist().index(ingredient['product_name']) if ingredient['product_name'] in products_df['Product Name'].tolist() else 0
                    )
                with col2:
                    quantity = st.number_input(
                        get_text("quantity", current_lang),
                        min_value=0.0,
                        step=0.1,
                        value=ingredient['quantity'],
                        key=f"qty_{i}"
                    )
                with col3:
                    unit_options = ["oz", "lb", "case", "each", "gallon", "liter", "quart", "grams"]
                    unit = st.selectbox(
                        get_text("unit", current_lang),
                        unit_options,
                        index=unit_options.index(ingredient['unit']) if ingredient['unit'] in unit_options else 0,
                        key=f"unit_{i}"
                    )
                with col4:
                    if st.button(get_text("remove", current_lang), key=f"remove_{i}"):
                        st.session_state.ingredients.pop(i)
                        st.rerun()
                
                # Update ingredient
                st.session_state.ingredients[i] = {
                    'product_name': product_name,
                    'quantity': quantity,
                    'unit': unit
                }
            
            # Add new ingredient button
            if st.button(get_text("add_ingredient", current_lang)):
                st.session_state.ingredients.append({
                    'product_name': products_df['Product Name'].iloc[0] if not products_df.empty else "",
                    'quantity': 1.0,
                    'unit': "oz"
                })
                st.rerun()
        
        # Recipe form
        with st.form("create_recipe_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                recipe_name = st.text_input(get_text("recipe_name", current_lang))
                description = st.text_area(get_text("description", current_lang))
                servings = st.number_input(get_text("servings", current_lang), min_value=1, value=4)
                prep_time = st.number_input(get_text("prep_time", current_lang), min_value=0, value=30)
            
            with col2:
                cook_time = st.number_input(get_text("cook_time", current_lang), min_value=0, value=45)
                
                # Category dropdown with predefined options
                category_options = [
                    "Main Course", "Appetizer", "Dessert", "Soup", "Salad", 
                    "Side Dish", "Beverage", "Sauce", "Dressing", "Marinade", "Prep Recipe", "Bar", "Other"
                ]
                
                # Get existing categories from recipes and add to options (excluding "Test")
                existing_categories = get_recipe_categories(recipes)
                for cat in existing_categories:
                    if cat not in category_options and cat != "Test":
                        category_options.append(cat)
                
                category = st.selectbox(
                    get_text("category", current_lang),
                    category_options,
                    index=0
                )
                
                instructions = st.text_area(get_text("cooking_instructions", current_lang))
            
            submitted = st.form_submit_button(get_text("save_recipe", current_lang))
            
            if submitted:
                if not recipe_name:
                    st.error(get_text("please_enter_name", current_lang))
                else:
                    recipe_data = {
                        'name': recipe_name,
                        'description': description,
                        'servings': servings,
                        'prep_time': prep_time,
                        'cook_time': cook_time,
                        'category': category,
                        'instructions': instructions,
                        'ingredients': st.session_state.ingredients.copy()
                    }
                    
                    success, message = save_recipe(recipe_data)
                    if success:
                        st.success(message)
                        # Clear ingredients for next recipe
                        st.session_state.ingredients = []
                        st.rerun()
                    else:
                        st.error(message)
    
    # Tab 2: View Recipes
    with tab2:
        st.subheader(get_text("view_all_recipes", current_lang))
        
        if not recipes:
            st.info(get_text("no_recipes_found", current_lang))
        else:
            # Filter by category
            categories = [get_text("all_categories", current_lang)] + get_recipe_categories(recipes)
            selected_category = st.selectbox(get_text("filter_by_category", current_lang), categories)
            
            # Filter recipes
            filtered_recipes = filter_recipes_by_category(recipes, selected_category)
            
            # Display recipes
            if filtered_recipes:
                st.write(get_text("showing_recipes", current_lang, 
                                count=len(filtered_recipes), 
                                category=selected_category))
                
                for recipe_name, recipe in filtered_recipes.items():
                    with st.expander(f"📋 {recipe_name}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**{get_text('description', current_lang)}:** {recipe.get('description', 'N/A')}")
                            st.write(f"**{get_text('servings', current_lang)}:** {recipe.get('servings', 'N/A')}")
                            st.write(f"**{get_text('category', current_lang)}:** {recipe.get('category', 'N/A')}")
                            st.write(f"**{get_text('prep_time', current_lang)}:** {recipe.get('prep_time', 'N/A')} min")
                            st.write(f"**{get_text('cook_time', current_lang)}:** {recipe.get('cook_time', 'N/A')} min")
                        
                        with col2:
                            st.write(f"**{get_text('total_recipe_cost', current_lang)}:** {format_currency(recipe.get('total_cost', 0))}")
                            st.write(f"**{get_text('ingredients', current_lang)}:**")
                            for ingredient in recipe.get('ingredients', []):
                                st.write(f"  • {ingredient['quantity']} {ingredient['unit']} {ingredient['product_name']}")
                        
                        if recipe.get('instructions'):
                            st.write(f"**{get_text('cooking_instructions', current_lang)}:**")
                            st.write(recipe['instructions'])
            else:
                st.info(get_text("no_recipes_category", current_lang, category=selected_category))
            
            # Summary statistics
            st.subheader("📊 " + get_text("summary", current_lang))
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(get_text("total_recipes", current_lang), len(recipes))
            
            with col2:
                total_cost = sum(recipe.get('total_cost', 0) for recipe in recipes.values())
                st.metric(get_text("total_recipe_cost", current_lang), format_currency(total_cost))
            
            with col3:
                avg_cost = total_cost / len(recipes) if recipes else 0
                st.metric(get_text("average_recipe_cost", current_lang), format_currency(avg_cost))
    
    # Tab 3: Edit Recipe
    with tab3:
        st.subheader(get_text("edit_recipe_title", current_lang))
        
        if not recipes:
            st.info(get_text("no_recipes_edit", current_lang))
        else:
            # Search functionality
            search_term = st.text_input(get_text("search_recipe", current_lang))
            
            # Filter recipes by search
            filtered_recipes = search_recipes(recipes, search_term)
            
            if filtered_recipes:
                recipe_to_edit = st.selectbox(get_text("select_recipe_edit", current_lang), 
                                            list(filtered_recipes.keys()))
                
                if recipe_to_edit:
                    recipe = filtered_recipes[recipe_to_edit]
                    st.write(get_text("editing_recipe", current_lang, name=recipe_to_edit))
                    
                    # Initialize edit ingredients - always load current recipe ingredients
                    st.session_state.edit_ingredients = recipe.get('ingredients', []).copy()
                    
                    # Edit ingredients outside of form
                    st.write("### " + get_text("ingredients", current_lang))
                    
                    # Debug: Show current ingredients
                    if st.session_state.edit_ingredients:
                        st.info(f"Found {len(st.session_state.edit_ingredients)} ingredients to edit")
                    else:
                        st.warning("No ingredients found in recipe")
                    
                    for i, ingredient in enumerate(st.session_state.edit_ingredients):
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        with col1:
                            # Check if product exists in current database
                            available_products = products_df['Product Name'].tolist()
                            current_product = ingredient['product_name']
                            
                            if current_product not in available_products:
                                st.warning(f"Product '{current_product}' not found in database")
                            
                            product_name = st.selectbox(
                                get_text("product", current_lang),
                                available_products,
                                key=f"edit_product_{i}",
                                index=available_products.index(current_product) if current_product in available_products else 0
                            )
                        with col2:
                            quantity = st.number_input(
                                get_text("quantity", current_lang),
                                min_value=0.0,
                                step=0.1,
                                value=ingredient['quantity'],
                                key=f"edit_qty_{i}"
                            )
                        with col3:
                            unit_options = ["oz", "lb", "case", "each", "gallon", "liter", "quart", "grams"]
                            unit = st.selectbox(
                                get_text("unit", current_lang),
                                unit_options,
                                index=unit_options.index(ingredient['unit']) if ingredient['unit'] in unit_options else 0,
                                key=f"edit_unit_{i}"
                            )
                        with col4:
                            if st.button(get_text("remove", current_lang), key=f"edit_remove_{i}"):
                                st.session_state.edit_ingredients.pop(i)
                                st.rerun()
                        
                        # Update ingredient
                        st.session_state.edit_ingredients[i] = {
                            'product_name': product_name,
                            'quantity': quantity,
                            'unit': unit
                        }
                    
                    # Add new ingredient button
                    if st.button(get_text("add_ingredient", current_lang), key="edit_add"):
                        st.session_state.edit_ingredients.append({
                            'product_name': products_df['Product Name'].iloc[0] if not products_df.empty else "",
                            'quantity': 1.0,
                            'unit': "oz"
                        })
                        st.rerun()
                    
                    # Edit recipe form
                    with st.form("edit_recipe_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            new_name = st.text_input(get_text("recipe_name", current_lang), value=recipe['name'])
                            new_description = st.text_area(get_text("description", current_lang), value=recipe.get('description', ''))
                            new_servings = st.number_input(get_text("servings", current_lang), min_value=1, value=recipe.get('servings', 4))
                            new_prep_time = st.number_input(get_text("prep_time", current_lang), min_value=0, value=recipe.get('prep_time', 30))
                        
                        with col2:
                            new_cook_time = st.number_input(get_text("cook_time", current_lang), min_value=0, value=recipe.get('cook_time', 45))
                            
                            # Category dropdown for edit form
                            edit_category_options = [
                                "Main Course", "Appetizer", "Dessert", "Soup", "Salad", 
                                "Side Dish", "Beverage", "Sauce", "Dressing", "Marinade", "Prep Recipe", "Bar", "Other"
                            ]
                            
                            # Get existing categories and add to options (excluding "Test")
                            existing_categories = get_recipe_categories(recipes)
                            for cat in existing_categories:
                                if cat not in edit_category_options and cat != "Test":
                                    edit_category_options.append(cat)
                            
                            # Find current category index
                            current_category = recipe.get('category', '')
                            category_index = 0
                            if current_category in edit_category_options:
                                category_index = edit_category_options.index(current_category)
                            
                            new_category = st.selectbox(
                                get_text("category", current_lang),
                                edit_category_options,
                                index=category_index
                            )
                            
                            new_instructions = st.text_area(get_text("cooking_instructions", current_lang), value=recipe.get('instructions', ''))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button(get_text("update_recipe", current_lang)):
                                updated_recipe = {
                                    'name': new_name,
                                    'description': new_description,
                                    'servings': new_servings,
                                    'prep_time': new_prep_time,
                                    'cook_time': new_cook_time,
                                    'category': new_category,
                                    'instructions': new_instructions,
                                    'ingredients': st.session_state.edit_ingredients.copy()
                                }
                                
                                success, message = update_recipe(recipe_to_edit, updated_recipe)
                                if success:
                                    st.success(message)
                                    # Clear edit ingredients
                                    st.session_state.edit_ingredients = []
                                    st.rerun()
                                else:
                                    st.error(message)
                        
                        with col2:
                            if st.form_submit_button(get_text("delete_recipe", current_lang), type="secondary"):
                                success, message = delete_recipe(recipe_to_edit)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
            else:
                st.info(get_text("no_recipes_match", current_lang))

if __name__ == "__main__":
    main()
