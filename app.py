"""
Streamlit CRUD Application for Supabase Database
Supports bulk upload, manual addition, update, and delete operations
"""

import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime
import json
from config import SUPABASE_URL, SUPABASE_KEY, validate_config

# Page configuration
st.set_page_config(
    page_title="Supabase CRUD Tool",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Supabase client
@st.cache_resource
def init_supabase():
    """Initialize and return Supabase client"""
    is_valid, message = validate_config()
    if not is_valid:
        st.error(message)
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

# Helper Functions
def get_tables():
    """Get list of tables from Supabase database"""
    try:
        # Query the information schema to get table names
        result = supabase.table('information_schema.tables').select('table_name').execute()
        return [row['table_name'] for row in result.data if row['table_name'] not in ['information_schema', 'pg_catalog']]
    except Exception as e:
        st.error(f"Could not fetch tables: {str(e)}")
        return []

def get_table_data(table_name, limit=100):
    """Fetch data from specified table"""
    try:
        response = supabase.table(table_name).select("*").limit(limit).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return pd.DataFrame()

def get_table_columns(table_name):
    """Get column names and types for a table"""
    try:
        response = supabase.table(table_name).select("*").limit(1).execute()
        if response.data:
            return list(response.data[0].keys())
        return []
    except Exception as e:
        st.error(f"Error fetching columns: {str(e)}")
        return []

def insert_record(table_name, data):
    """Insert a single record into the table"""
    try:
        response = supabase.table(table_name).insert(data).execute()
        return True, "Record inserted successfully!"
    except Exception as e:
        return False, f"Error inserting record: {str(e)}"

def bulk_insert_records(table_name, dataframe):
    """Bulk insert records from a dataframe"""
    try:
        records = dataframe.to_dict('records')
        response = supabase.table(table_name).insert(records).execute()
        return True, f"Successfully inserted {len(records)} records!"
    except Exception as e:
        return False, f"Error in bulk insert: {str(e)}"

def update_record(table_name, record_id, id_column, data):
    """Update a record in the table"""
    try:
        response = supabase.table(table_name).update(data).eq(id_column, record_id).execute()
        return True, "Record updated successfully!"
    except Exception as e:
        return False, f"Error updating record: {str(e)}"

def delete_record(table_name, record_id, id_column):
    """Delete a record from the table"""
    try:
        response = supabase.table(table_name).delete().eq(id_column, record_id).execute()
        return True, "Record deleted successfully!"
    except Exception as e:
        return False, f"Error deleting record: {str(e)}"

# Main App
def main():
    st.title("🗄️ Supabase CRUD Tool")
    st.markdown("---")

    # Sidebar for table selection
    with st.sidebar:
        st.header("📊 Database Configuration")

        # Manual table name input
        st.subheader("Select/Enter Table")
        table_name = st.text_input(
            "Table Name",
            placeholder="Enter your table name",
            help="Enter the exact name of your Supabase table"
        )

        if table_name:
            st.success(f"Selected table: **{table_name}**")
        else:
            st.warning("Please enter a table name to begin")

        st.markdown("---")
        st.info("💡 Make sure your table exists in Supabase before performing operations")

    # Main content area
    if not table_name:
        st.info("👈 Please enter a table name in the sidebar to get started")
        return

    # Operation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 View Data",
        "➕ Add Record",
        "📝 Update Record",
        "🗑️ Delete Record",
        "📤 Bulk Upload"
    ])

    # Tab 1: View Data (READ)
    with tab1:
        st.header("📖 View Data")

        col1, col2 = st.columns([3, 1])
        with col1:
            limit = st.slider("Number of records to display", 10, 1000, 100)
        with col2:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()

        df = get_table_data(table_name, limit)

        if not df.empty:
            st.success(f"Found {len(df)} records")

            # Search/Filter functionality
            search_term = st.text_input("🔍 Search in data", placeholder="Enter search term...")
            if search_term:
                mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                df = df[mask]
                st.info(f"Showing {len(df)} filtered records")

            # Display dataframe
            st.dataframe(df, use_container_width=True, height=400)

            # Download options
            col1, col2 = st.columns(2)
            with col1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col2:
                excel_buffer = pd.ExcelWriter(f"{table_name}.xlsx", engine='openpyxl')
                df.to_excel(excel_buffer, index=False)
                excel_buffer.close()

        else:
            st.warning("No data found in this table")

    # Tab 2: Add Record (CREATE)
    with tab2:
        st.header("➕ Add New Record")

        columns = get_table_columns(table_name)

        if columns:
            st.info(f"Available columns: {', '.join(columns)}")

            with st.form("add_record_form"):
                st.subheader("Enter Record Details")

                record_data = {}
                cols = st.columns(2)

                for idx, col in enumerate(columns):
                    with cols[idx % 2]:
                        if col.lower() in ['id', 'created_at', 'updated_at']:
                            st.text_input(
                                f"{col} (auto-generated)",
                                disabled=True,
                                help="This field is auto-generated"
                            )
                        else:
                            record_data[col] = st.text_input(
                                col,
                                help=f"Enter value for {col}"
                            )

                submitted = st.form_submit_button("✅ Add Record", use_container_width=True)

                if submitted:
                    # Remove empty values and auto-generated fields
                    clean_data = {k: v for k, v in record_data.items()
                                if v and k.lower() not in ['id', 'created_at', 'updated_at']}

                    if clean_data:
                        success, message = insert_record(table_name, clean_data)
                        if success:
                            st.success(message)
                            st.balloons()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please fill in at least one field")
        else:
            st.error("Could not retrieve table columns. Please check if the table exists.")

    # Tab 3: Update Record (UPDATE)
    with tab3:
        st.header("📝 Update Record")

        df = get_table_data(table_name, 1000)

        if not df.empty:
            columns = list(df.columns)

            # Select ID column
            id_column = st.selectbox(
                "Select ID Column",
                columns,
                help="Choose the column that contains unique identifiers"
            )

            # Select record to update
            record_id = st.selectbox(
                "Select Record to Update",
                df[id_column].tolist(),
                help="Choose the record you want to update"
            )

            if record_id is not None:
                # Get current record data
                current_record = df[df[id_column] == record_id].iloc[0].to_dict()

                st.info("Current values are pre-filled. Modify the fields you want to update.")

                with st.form("update_record_form"):
                    st.subheader(f"Update Record: {record_id}")

                    update_data = {}
                    cols = st.columns(2)

                    for idx, col in enumerate(columns):
                        with cols[idx % 2]:
                            if col == id_column:
                                st.text_input(
                                    f"{col} (ID - cannot be changed)",
                                    value=str(current_record[col]),
                                    disabled=True
                                )
                            else:
                                current_value = current_record.get(col, "")
                                update_data[col] = st.text_input(
                                    col,
                                    value=str(current_value) if current_value is not None else "",
                                    help=f"Update value for {col}"
                                )

                    submitted = st.form_submit_button("✅ Update Record", use_container_width=True)

                    if submitted:
                        # Remove empty values and ID field
                        clean_data = {k: v for k, v in update_data.items()
                                    if v and k != id_column}

                        if clean_data:
                            success, message = update_record(table_name, record_id, id_column, clean_data)
                            if success:
                                st.success(message)
                                st.balloons()
                            else:
                                st.error(message)
                        else:
                            st.warning("No changes detected")
        else:
            st.warning("No records found in this table")

    # Tab 4: Delete Record (DELETE)
    with tab4:
        st.header("🗑️ Delete Record")

        df = get_table_data(table_name, 1000)

        if not df.empty:
            columns = list(df.columns)

            # Select ID column
            id_column = st.selectbox(
                "Select ID Column ",
                columns,
                help="Choose the column that contains unique identifiers",
                key="delete_id_col"
            )

            # Select record to delete
            record_id = st.selectbox(
                "Select Record to Delete",
                df[id_column].tolist(),
                help="Choose the record you want to delete",
                key="delete_record_id"
            )

            if record_id is not None:
                # Show record details
                current_record = df[df[id_column] == record_id].iloc[0].to_dict()

                st.warning("⚠️ You are about to delete the following record:")
                st.json(current_record)

                col1, col2, col3 = st.columns([1, 1, 2])

                with col1:
                    if st.button("🗑️ Delete Record", type="primary", use_container_width=True):
                        success, message = delete_record(table_name, record_id, id_column)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

                with col2:
                    if st.button("Cancel", use_container_width=True):
                        st.info("Delete operation cancelled")
        else:
            st.warning("No records found in this table")

    # Tab 5: Bulk Upload
    with tab5:
        st.header("📤 Bulk Upload")

        st.info("Upload CSV or Excel files to bulk insert records into your table")

        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload a CSV or Excel file with data to insert"
        )

        if uploaded_file is not None:
            try:
                # Read file based on type
                if uploaded_file.name.endswith('.csv'):
                    df_upload = pd.read_csv(uploaded_file)
                else:
                    df_upload = pd.read_excel(uploaded_file)

                st.success(f"✅ File loaded successfully! Found {len(df_upload)} rows")

                # Preview data
                st.subheader("📋 Data Preview")
                st.dataframe(df_upload.head(10), use_container_width=True)

                # Show column mapping
                st.subheader("🔗 Column Mapping")
                table_columns = get_table_columns(table_name)

                if table_columns:
                    st.info(f"Table columns: {', '.join(table_columns)}")

                    file_columns = df_upload.columns.tolist()
                    st.info(f"File columns: {', '.join(file_columns)}")

                    # Check if columns match
                    matching_cols = set(file_columns) & set(table_columns)
                    if matching_cols:
                        st.success(f"Matching columns: {', '.join(matching_cols)}")

                    # Option to map columns
                    map_columns = st.checkbox("Map columns manually", value=False)

                    if map_columns:
                        column_mapping = {}
                        st.write("Map file columns to table columns:")
                        cols = st.columns(2)

                        for idx, file_col in enumerate(file_columns):
                            with cols[idx % 2]:
                                column_mapping[file_col] = st.selectbox(
                                    f"{file_col} →",
                                    ["Skip"] + table_columns,
                                    key=f"map_{file_col}"
                                )

                        # Apply mapping
                        if st.button("Apply Mapping"):
                            mapped_df = pd.DataFrame()
                            for file_col, table_col in column_mapping.items():
                                if table_col != "Skip":
                                    mapped_df[table_col] = df_upload[file_col]
                            df_upload = mapped_df
                            st.success("Column mapping applied!")
                            st.dataframe(df_upload.head(), use_container_width=True)

                    # Upload options
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        # Clean data options
                        remove_empty = st.checkbox("Remove rows with empty values", value=False)
                        if remove_empty:
                            df_upload = df_upload.dropna()
                            st.info(f"Rows after cleaning: {len(df_upload)}")

                    with col2:
                        upload_limit = st.number_input(
                            "Limit rows to upload",
                            min_value=1,
                            max_value=len(df_upload),
                            value=len(df_upload)
                        )

                    df_upload = df_upload.head(upload_limit)

                    # Upload button
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 1, 2])

                    with col1:
                        if st.button("📤 Upload to Supabase", type="primary", use_container_width=True):
                            with st.spinner("Uploading..."):
                                success, message = bulk_insert_records(table_name, df_upload)
                                if success:
                                    st.success(message)
                                    st.balloons()
                                else:
                                    st.error(message)

                    with col2:
                        if st.button("Clear", use_container_width=True):
                            st.rerun()

                else:
                    st.error("Could not retrieve table columns")

            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
        else:
            st.info("👆 Upload a file to begin bulk insert")

            # Show sample format
            with st.expander("📄 View Sample File Format"):
                columns = get_table_columns(table_name)
                if columns:
                    sample_df = pd.DataFrame(columns=columns)
                    st.write("Your CSV/Excel file should have columns matching your table:")
                    st.dataframe(sample_df, use_container_width=True)

                    # Download sample template
                    csv_sample = sample_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Template CSV",
                        data=csv_sample,
                        file_name=f"{table_name}_template.csv",
                        mime="text/csv"
                    )

if __name__ == "__main__":
    main()
