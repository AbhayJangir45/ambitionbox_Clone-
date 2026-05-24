from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import os
import traceback

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    try:
        df = pd.read_csv("all_ambition_data.csv")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return "Error loading data. Check if all_ambition_data.csv exists.", 500
    
    if request.method == 'POST':
        location = request.form.get('location')
        industry = request.form.get('industry')
        rating = request.form.get('rating')
        output = request.form.get('output')
        
        # Filter the dataframe
        try:
            if location:
                df = df[df['Location'].str.contains(location, na=False)]
            if industry:
                df = df[df['Industry'].str.contains(industry, na=False)]
            if rating:
                if rating == '1':
                    df = df[df['Rating'] == 1.0]
                elif rating == '1+':
                    pass  # all ratings 1-5
                elif rating == '2+':
                    df = df[df['Rating'] >= 2.0]
                elif rating == '3+':
                    df = df[df['Rating'] >= 4.0]  # 4 to 5 as per "3+ contai 4 to 5"
                elif rating == '4+':
                    df = df[df['Rating'] >= 4.0]
                elif rating == '5':
                    df = df[df['Rating'] == 5.0]
        except Exception as e:
            print(f"Filtering error: {e}")
        
        if output == 'Show Table':
            return render_template("table_page.html", data=df.to_dict('records'))
        elif output == 'Show Visualizations':
            try:
                # Clear previous graphs
                for i in range(1,7):
                    graph_path = f'static/graph{i}.png'
                    if os.path.exists(graph_path):
                        os.remove(graph_path)
                
                # Process data
                def parse_number(s):
                    if pd.isna(s) or s == '--':
                        return 0
                    s = str(s).strip()
                    if 'k' in s.lower():
                        return float(s.replace('k', '').replace('K', '')) * 1000
                    elif 'l' in s.lower():
                        return float(s.replace('l', '').replace('L', '')) * 100000
                    else:
                        return float(s)

                df['Jobs_parsed'] = df['Jobs'].apply(parse_number)
                df['Salery_parsed'] = df['Salery'].apply(parse_number)
                df['Review_parsed'] = df['Review'].apply(parse_number)

                os.makedirs('static', exist_ok=True)

                # Graph 1: Top 10 companies by rating
                if len(df) > 0:
                    plt.figure(figsize=(8,6))
                    top10 = df.nlargest(10, 'Rating')
                    plt.bar(top10['Company_Names'], top10['Rating'])
                    plt.title('Top 10 Companies by Rating')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    plt.savefig('static/graph1.png')
                    plt.close()

                    # Graph 2: Rating vs Number of Reviews
                    plt.figure(figsize=(8,6))
                    plt.scatter(df['Review_parsed'], df['Rating'])
                    plt.title('Rating vs Number of Reviews')
                    plt.xlabel('Reviews')
                    plt.ylabel('Rating')
                    plt.tight_layout()
                    plt.savefig('static/graph2.png')
                    plt.close()

                    # Graph 3: Industry Distribution
                    industry_counts = df['Industry'].value_counts()
                    if len(industry_counts) > 0:
                        plt.figure(figsize=(8,6))
                        plt.pie(industry_counts.values, labels=industry_counts.index, autopct='%1.1f%%')
                        plt.title('Industry Distribution')
                        plt.tight_layout()
                        plt.savefig('static/graph3.png')
                        plt.close()

                    # Graph 4: Rating Distribution
                    plt.figure(figsize=(8,6))
                    plt.hist(df['Rating'], bins=10)
                    plt.title('Rating Distribution')
                    plt.xlabel('Rating')
                    plt.ylabel('Frequency')
                    plt.tight_layout()
                    plt.savefig('static/graph4.png')
                    plt.close()

                    # Graph 5: Average Rating by Industry
                    avg_rating = df.groupby('Industry')['Rating'].mean().reset_index()
                    if len(avg_rating) > 0:
                        plt.figure(figsize=(8,6))
                        plt.bar(avg_rating['Industry'], avg_rating['Rating'])
                        plt.title('Average Rating by Industry')
                        plt.xticks(rotation=45, ha='right')
                        plt.tight_layout()
                        plt.savefig('static/graph5.png')
                        plt.close()

                    # Graph 6: Jobs vs Salary
                    plt.figure(figsize=(8,6))
                    plt.scatter(df['Jobs_parsed'], df['Salery_parsed'])
                    plt.title('Jobs vs Salary')
                    plt.xlabel('Jobs')
                    plt.ylabel('Salary')
                    plt.tight_layout()
                    plt.savefig('static/graph6.png')
                    plt.close()

                graphs = ['graph1.png', 'graph2.png', 'graph3.png', 'graph4.png', 'graph5.png', 'graph6.png']

                return render_template("visualization_page.html", graphs=graphs)
            except Exception as e:
                print(f"Visualization error: {traceback.format_exc()}")
                return f"Error generating visualizations: {str(e)}", 500
        else:
            return render_template("table_page.html", data=df.to_dict('records'))
    
    # For GET
    try:
        locations = df['Location'].dropna().unique()
        industries = df['Industry'].dropna().unique()
        ratings = ['1', '1+', '2+', '3+', '4+', '5']
    except:
        locations = []
        industries = []
        ratings = []
    
    return render_template('home.html', locations=locations, industries=industries, ratings=ratings)

@app.route('/visualizations')
def visualizations():
    return home()  

if __name__ == '__main__':
    app.run(debug=True, port=6500, host='127.0.0.1')
