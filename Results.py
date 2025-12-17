from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from IPython.display import display, HTML
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
import os

# Style configuration for nicer plots
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = [10, 6]

llm_colors = {
    'ChatGPT': "#25D899",  # OpenAI Teal
    'Claude':  "#FF9436",  # Anthropic Clay/Orange
    'Gemini':  '#4285F4'   # Google Blue
}


def load_data(base_dir, models):
    all_records = []

    for llm in models:
        llm_path = os.path.join(base_dir, llm)
        
        if not os.path.exists(llm_path):
            print(f"Warning: Path not found for {llm}")
            continue
            
        # Walk through the directory structure
        for root, _, files in os.walk(llm_path):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    
                    # Determine the category based on folder structure
                    # Ex: Results/Gemini/Synthetic/Single: Synthetic -> Single
                    rel_path = os.path.relpath(root, llm_path)
                    category = rel_path.replace(os.path.sep, " -> ")
                    if category == ".": category = "Uncategorized"

                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                            # Extract specific smell results
                            for smell in data.get('smell_analysis', []):
                                record = {
                                    'LLM': llm,
                                    'Category': category,
                                    'File': data.get('file_name'),
                                    'Rule_ID': smell.get('rule_id'),
                                    'Actual': smell.get('actual'),
                                    'Detected': smell.get('detected'),
                                    'Justification': smell.get('justification')
                                }
                                all_records.append(record)
                    except Exception as e:
                        print(f"Error reading {full_path}: {e}")

    return pd.DataFrame(all_records)


def calculate_metrics(dataframe, grouping_col=None):
    """
    Calculates Accuracy, Precision, Recall, and F1 for given data.
    """
    results = []
    
    # Identify unique groups (e.g., unique LLMs)
    groups = dataframe[grouping_col].unique() if grouping_col else [None]
    
    for group in groups:
        subset = dataframe[dataframe[grouping_col] == group] if group else dataframe
        
        y_true = subset['Actual'].astype(int)
        y_pred = subset['Detected'].astype(int)
        
        metrics = {
            'Accuracy': accuracy_score(y_true, y_pred),
            'Precision': precision_score(y_true, y_pred, zero_division=0),
            'Recall': recall_score(y_true, y_pred, zero_division=0),
            'F1-Score': f1_score(y_true, y_pred, zero_division=0),
            'Sample_Size': len(subset)
        }
        
        if grouping_col:
            metrics[grouping_col] = group
            
        results.append(metrics)
        
    return pd.DataFrame(results)


def plot_confusion_matrix_per_llm(dataframe, title_prefix="Overall"):
    """
    Plots a row of confusion matrices, one for each LLM.
    """
    llms = dataframe['LLM'].unique()
    _, axes = plt.subplots(1, len(llms), figsize=(5 * len(llms), 4))
    
    if len(llms) == 1: axes = [axes] # Handle single case

    for ax, llm in zip(axes, llms):
        subset = dataframe[dataframe['LLM'] == llm]
        cm = confusion_matrix(subset['Actual'], subset['Detected'], labels=[True, False])
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax, 
                    xticklabels=['Detected', 'Not Detected'], 
                    yticklabels=['Actual', 'Not Actual'])
        ax.set_title(f"{llm}")
        ax.set_xlabel('Prediction')
        ax.set_ylabel('Ground Truth')
    
    plt.suptitle(f'{title_prefix} Confusion Matrices', y=1.05, fontsize=16)
    plt.tight_layout()
    plt.show()
    # Force a blank space after the plot
    display(HTML("<br>"))


def plot_benchmark_bars(metrics_df, title):
    """
    Plots a grouped bar chart comparing LLMs across metrics.
    """
    # Melt the dataframe for Seaborn plotting
    melted = metrics_df.melt(id_vars=['LLM'], 
                             value_vars=['Accuracy', 'Precision', 'Recall', 'F1-Score'], 
                             var_name='Metric', value_name='Score')
    
    plt.figure(figsize=(10, 6))

    # barplot with LLM Colors
    ax = sns.barplot(
        data=melted, 
        x='Metric', 
        y='Score', 
        hue='LLM', 
        palette=llm_colors
    )
    
    plt.title(title, fontsize=15)
    plt.ylim(0, 1.05)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add numbers on top of bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f')
        
    plt.show()
    # Force a blank space after the plot
    display(HTML("<br>"))



def plot_custom_aggregates(df, custom_aggregates):
    for group_name, target_categories in custom_aggregates.items():
        print(" ")
        print(f"--- Analysis for {group_name} ---")
        print(" ")
    
        # Filter the main dataframe for only the categories in this group
        group_df = df[df['Category'].isin(target_categories)]
    
        if group_df.empty:
            print(f"No data found for {group_name}. Check category names.")
            continue
        
        # 1. Calculate Metrics
        group_metrics = calculate_metrics(group_df, grouping_col='LLM')
        display(group_metrics)
    
        # 2. Plot Bar Chart
        plot_benchmark_bars(group_metrics, f"Performance: {group_name}")
    
        # 3. Plot Confusion Matrices
        plot_confusion_matrix_per_llm(group_df, title_prefix=group_name)
        # Force a blank space after the plot
        display(HTML("<br>"))


def plot_per_category(df, target_order):
    # Get list of what actually exists in the data (to avoid errors if a folder is empty)
    available_categories = set(df['Category'].unique())

    for cat in target_order:
        # Skip if this category isn't in your loaded data
        if cat not in available_categories:
            print(f"Skipping {cat} (Not found in loaded data)")
            continue
        
        print(" ")
        print(f"--- Analysis for {cat} ---")
        print(" ")
    
        # Filter data for this category
        cat_df = df[df['Category'] == cat]
    
        # Calculate Metrics
        cat_metrics = calculate_metrics(cat_df, grouping_col='LLM')
        display(cat_metrics)
    
        # Plot Bar Chart
        plot_benchmark_bars(cat_metrics, f"Performance: {cat}")
    
        # Plot Confusion Matrix
        plot_confusion_matrix_per_llm(cat_df, title_prefix=cat)
        # Force a blank space after the plot
        display(HTML("<br>"))



def plot_hardest_smells(df):
    # Calculate Recall per Rule per LLM
    rule_metrics_list = []
    unique_rules = sorted(df['Rule_ID'].unique())

    for rule in unique_rules:
        subset = df[df['Rule_ID'] == rule]
        # We only care about rules that actually existed (Actual=True) to calculate Recall
        if subset['Actual'].sum() > 0: 
            m = calculate_metrics(subset, grouping_col='LLM')
            m['Rule_ID'] = rule
            rule_metrics_list.append(m)

    if rule_metrics_list:
        rule_df = pd.concat(rule_metrics_list)
    
        # Create Pivot Table for Heatmap
        heatmap_data = rule_df.pivot(index='Rule_ID', columns='LLM', values='Recall')
    
        # Plot
        plt.figure(figsize=(10, 10))
        sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", vmin=0, vmax=1, fmt='.2f', linewidths=0.5)
    
        plt.title('Recall Rate by Smell Rule (Darker Red = Better Detection)', fontsize=14)
        plt.ylabel("Smell Rule ID")
        plt.yticks(rotation=0) 

        plt.show()
    else:
        print("Not enough data to calculate per-rule recall.")
    # Force a blank space after the plot
    display(HTML("<br>"))


def plot_hallucinations(df, llm_models):
    # 1. Filter for False Positives (Actual=False, Detected=True)
    fp_df = df[(df['Actual'] == False) & (df['Detected'] == True)]

    # 2. Count occurrences per LLM
    # We reindex to ensure all LLMs show up even if they have 0 hallucinations
    fp_counts = fp_df['LLM'].value_counts().reindex(llm_models, fill_value=0).reset_index()
    fp_counts.columns = ['LLM', 'False_Positives']

    # 3. Plot
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(
        data=fp_counts, 
        x='LLM', 
        y='False_Positives', 
        hue='LLM', 
        palette=llm_colors,
        legend=True # Ensure legend is generated
    )

    # Title
    plt.title('Total Hallucinations (False Positives) - Lower is Better', fontsize=14)
    plt.ylabel("Nr of False Positives")

    # Add the numbers on top of the bars
    for container in ax.containers:
        ax.bar_label(container)

    # --- THE MISSING RIGHT SIDE PANEL (LEGEND) ---
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='LLM Model')
    # ---------------------------------------------

    plt.tight_layout()
    plt.show()
    # Force a blank space after the plot
    display(HTML("<br>"))


def plot_paranoia_heatmap(df):
    # 1. DATA PREPARATION
    # We need to look at cases where the smell was NOT actually present (Actual = False)
    negatives_df = df[df['Actual'] == False]

    if not negatives_df.empty:
        # Calculate FPR: Mean of 'Detected' on negative samples.
        # If Actual is False, and Detected is True (1), mean goes up. 
        # If Detected is False (0), mean stays 0.
        fpr_data = negatives_df.pivot_table(
            index='Rule_ID', 
            columns='LLM', 
            values='Detected', 
            aggfunc='mean'  # This calculates False Positives / Total Negatives
        )

        # 2. PLOTTING
        plt.figure(figsize=(12, 10))

        sns.heatmap(
            fpr_data, 
            annot=True,       
            fmt=".2f",        
            cmap="Reds",      # White (0.0) -> Red (High Error)
            vmin=0, vmax=1,   
            linewidths=0.5,   
            linecolor='gray'
        )

        plt.title('Paranoia Check: False Positive Rate (Dark Red = High Hallucination)', fontsize=14, pad=20)
        plt.xlabel("LLM Model", fontsize=12)
        plt.ylabel("UML Smell Rule", fontsize=12)
    
        # Keep labels horizontal
        plt.yticks(rotation=0)
    
        plt.tight_layout()
        plt.show()

    else:
        print("No negative samples found (Everything was a smell?), cannot calc False Positive Rate.")
    # Force a blank space after the plot
    display(HTML("<br>"))


def plot_strategy_map(df):
    # 1. Calculate Overall Metrics
    strategy_metrics = calculate_metrics(df, grouping_col='LLM')

    # 2. PLOTTING
    plt.figure(figsize=(10, 8))

    # Create the scatter plot
    ax = sns.scatterplot(
        data=strategy_metrics, 
        x='Precision', 
        y='Recall', 
        hue='LLM', 
        s=400, # Make dots big
        palette=llm_colors,
        edgecolor='black'
    )

    # 3. Add Labels to the dots
    for i in range(strategy_metrics.shape[0]):
        plt.text(
            x=strategy_metrics.Precision[i]+0.01, 
            y=strategy_metrics.Recall[i]+0.01, 
            s=strategy_metrics.LLM[i], 
            fontdict=dict(color='black', size=12, weight='bold')
        )

    # 4. Add "Zone" Annotations for context
    plt.text(0.95, 0.1, "THE SAFE ZONE\n(Conservative)\nHigh Precision, Low Recall", 
            horizontalalignment='right', color='green', alpha=0.5, weight='bold')

    plt.text(0.1, 0.9, "THE PARANOID ZONE\n(Aggressive)\nLow Precision, High Recall", 
             horizontalalignment='left', color='red', alpha=0.5, weight='bold')

    plt.text(0.95, 0.95, "THE IDEAL ZONE\n(Perfect)", 
             horizontalalignment='right', color='gold', alpha=0.8, weight='bold')

    # Style
    plt.title('LLM Strategy Map: Who is playing it safe?', fontsize=16)
    plt.xlim(0, 1.05)
    plt.ylim(0, 1.05)
    plt.grid(True, linestyle='--')
    plt.axvline(0.5, color='gray', linestyle=':', alpha=0.5) # Center crosshair
    plt.axhline(0.5, color='gray', linestyle=':', alpha=0.5)

    plt.show()

