import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Connect to MySQL database using SQLAlchemy
def get_connection():
    connection_string = "mysql+mysqlconnector://root:Prachi%402024@127.0.0.1/RED_BUS_DETAILS"
    engine = create_engine(connection_string)
    return engine

# Function to fetch unique route names from the database
def fetch_route_names(engine):
    query = "SELECT DISTINCT Route_Name FROM red_bus_details ORDER BY Route_Name"
    route_names = pd.read_sql(query, engine)
    return route_names['Route_Name'].tolist()

# Function to fetch data based on selected route and price sort order
def fetch_data(engine, route_name, price_sort_order):
    price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
    sql_query = f"""
        SELECT * FROM red_bus_details 
        WHERE Route_Name = %s 
        ORDER BY Star_Rating DESC, Price {price_sort_order_sql}
    """
    df = pd.read_sql_query(sql_query, engine, params=(route_name,))
    return df

# Add custom CSS to style the background and headers
def add_custom_css():
    st.markdown("""
        <style>
        /* Background color */
        .stApp {
            background-color: #f5f5f5;
        }
        /* Header Styling */
        .stHeader {
            color: #e63946;
            text-align: center;
            font-size: 50px;
        }
        /* Subheader Styling */
        .stSubHeader {
            color: #457b9d;
            text-align: center;
            font-size: 30px;
        }
        </style>
        """, unsafe_allow_html=True)

# Main Streamlit app
def main():
    # Add custom CSS
    add_custom_css()

    # Header
    st.markdown("<h1 class='stHeader'>BOOK TICKETS NOW!!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='stSubHeader'>Get the Best Option Available</h2>", unsafe_allow_html=True)

    # Establish database connection
    engine = get_connection()

    try:
        # Sidebar for Route Selection
        st.sidebar.markdown("<h3 style='color:#e63946;'>Select Route and Preferences</h3>", unsafe_allow_html=True)
        
        route_names = fetch_route_names(engine)
        selected_route = st.sidebar.selectbox('Select Route Name', route_names)

        # Sidebar - Selectbox for sorting preference
        price_sort_order = st.sidebar.selectbox('Sort by Price', ['Low to High', 'High to Low'])

        if selected_route:
            st.markdown(f"<h3 style='color:#1d3557;'>You selected: {selected_route}</h3>", unsafe_allow_html=True)

            # Fetch data based on selected Route_Name and price sort order
            data = fetch_data(engine, selected_route, price_sort_order)

            if not data.empty:
                st.markdown(f"<h4 style='color:#2a9d8f;'>Bus Details for Route: {selected_route}</h4>", unsafe_allow_html=True)
                st.write(data)
            else:
                st.markdown(f"<h4 style='color:#f4a261;'>No data found for Route: {selected_route}</h4>", unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"An error occurred: {e}")

    finally:
        engine.dispose()  # Ensure the connection is closed

if __name__ == '__main__':
    main()
