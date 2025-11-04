# Supabase CRUD Tool with Streamlit

A powerful web-based interface for performing CRUD (Create, Read, Update, Delete) operations on Supabase databases with support for bulk uploads via CSV and Excel files.

## Features

- **View Data**: Browse and search through your database tables with pagination
- **Add Records**: Manually add individual records through an intuitive form interface
- **Update Records**: Edit existing records with pre-filled values
- **Delete Records**: Remove records with confirmation preview
- **Bulk Upload**: Upload multiple records at once via CSV or Excel files
- **Column Mapping**: Automatically map file columns to database columns
- **Data Export**: Download table data as CSV or Excel files
- **Search & Filter**: Search across all columns in real-time

## Prerequisites

- Python 3.8 or higher
- A Supabase account and project
- Supabase URL and API key

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
```

4. Edit the `.env` file and add your Supabase credentials:
```
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
```

## Getting Your Supabase Credentials

1. Go to your [Supabase Dashboard](https://app.supabase.com/)
2. Select your project
3. Click on the "Settings" icon (gear icon) in the sidebar
4. Go to "API" section
5. Copy your:
   - **Project URL** (paste as SUPABASE_URL)
   - **anon/public key** (paste as SUPABASE_KEY)

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown (typically `http://localhost:8501`)

3. Enter your table name in the sidebar

4. Choose an operation from the tabs:
   - **View Data**: Browse and search your data
   - **Add Record**: Create new records manually
   - **Update Record**: Edit existing records
   - **Delete Record**: Remove records
   - **Bulk Upload**: Upload CSV or Excel files

## Bulk Upload Instructions

### CSV Format
Your CSV file should have column headers that match your database table columns:

```csv
name,email,age,city
John Doe,john@example.com,30,New York
Jane Smith,jane@example.com,25,Los Angeles
```

### Excel Format
Your Excel file should have:
- Column headers in the first row
- Data starting from the second row
- Column names matching your database table

### Upload Process

1. Go to the "Bulk Upload" tab
2. Click "Browse files" and select your CSV or Excel file
3. Preview the data to ensure it's correct
4. (Optional) Use column mapping if your file columns don't match database columns
5. (Optional) Enable "Remove rows with empty values" to clean data
6. Click "Upload to Supabase" to insert records

## Features in Detail

### View Data
- Display up to 1000 records at once
- Real-time search across all columns
- Export data as CSV or Excel
- Refresh data with a single click

### Add Record
- Dynamic form generation based on table schema
- Auto-detects and disables auto-generated fields (id, created_at, updated_at)
- Input validation

### Update Record
- Select record by any column (typically ID)
- Pre-filled form with current values
- Only modified fields are updated

### Delete Record
- Select record to delete
- Preview record details before deletion
- Confirmation required before deletion

### Bulk Upload
- Support for CSV and Excel files (.csv, .xlsx, .xls)
- Data preview before upload
- Column mapping interface
- Option to clean empty rows
- Limit number of rows to upload
- Download template file with correct columns

## Security Notes

- Never commit your `.env` file to version control
- Use the anon/public key for public applications
- For sensitive operations, consider using Row Level Security (RLS) in Supabase
- Implement proper authentication for production use

## Troubleshooting

### "Missing Supabase credentials" error
- Ensure your `.env` file exists in the project root
- Verify that SUPABASE_URL and SUPABASE_KEY are correctly set

### "Could not fetch tables" error
- Check that your Supabase credentials are correct
- Verify that your table exists in Supabase
- Ensure your API key has the necessary permissions

### Bulk upload fails
- Verify column names match between file and database
- Check that data types are compatible
- Ensure required fields are not empty
- Try using column mapping feature

### "Table not found" error
- Double-check the table name spelling
- Ensure the table exists in your Supabase project
- Verify your API key has access to the table

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── config.py              # Configuration and environment setup
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Technologies Used

- **Streamlit**: Web application framework
- **Supabase**: Backend database and API
- **Pandas**: Data manipulation and CSV/Excel handling
- **OpenPyXL**: Excel file support
- **Python-dotenv**: Environment variable management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

## Roadmap

Future enhancements planned:
- [ ] Authentication and user management
- [ ] Batch update operations
- [ ] Advanced filtering and sorting
- [ ] Data validation rules
- [ ] Audit logging
- [ ] Multi-table operations
- [ ] Database schema viewer
- [ ] SQL query interface
- [ ] Data import from other sources (Google Sheets, APIs)
- [ ] Scheduled bulk uploads

## Acknowledgments

Built with Streamlit and powered by Supabase.
