#!/usr/bin/env python3
"""
Health Data Analysis Script
Analyze walking steps, sleep, and heart rate data from Amazfit Band 3
Similar to: https://bagustris.blogspot.com/2021/05/data-jalan-kaki-tidur-dan-detak-jantung.html
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# File paths
ACTIVITY_FILE = 'ACTIVITY/ACTIVITY_1767766216945.csv'
SLEEP_FILE = 'SLEEP/SLEEP_1767766217289.csv'
HEARTRATE_FILE = 'HEARTRATE/HEARTRATE_1767766218082.csv'

def load_activity_data():
    """Load and process activity data"""
    df = pd.read_csv(ACTIVITY_FILE)
    df['date'] = pd.to_datetime(df['date'])
    # Remove rows with steps less than 1000 (insufficient activity)
    df = df[df['steps'] >= 1000]
    return df

def load_sleep_data():
    """Load and process sleep data"""
    # Read CSV with special handling for the naps column which contains JSON
    df = pd.read_csv(SLEEP_FILE, escapechar='\\')
    df['date'] = pd.to_datetime(df['date'])
    df['start'] = pd.to_datetime(df['start'])
    df['stop'] = pd.to_datetime(df['stop'])
    
    # Calculate total sleep time in minutes
    df['totalSleepTime'] = df['deepSleepTime'] + df['shallowSleepTime'] + df['REMTime']
    
    # Remove rows with sleep less than 4 hours (240 minutes)
    df = df[df['totalSleepTime'] >= 240]
    
    # Extract bed time and wake time hours
    df['bedTime_hour'] = df['start'].dt.hour + df['start'].dt.minute / 60
    df['wakeTime_hour'] = df['stop'].dt.hour + df['stop'].dt.minute / 60
    
    return df

def load_heartrate_data():
    """Load and process heart rate data"""
    df = pd.read_csv(HEARTRATE_FILE)
    df['time'] = pd.to_datetime(df['time'])
    # Remove outliers (very low or very high heart rates)
    df = df[(df['heartRate'] >= 40) & (df['heartRate'] <= 200)]
    return df

def plot_activity_monthly(df):
    """Plot monthly activity statistics"""
    # Add year-month column
    df['year_month'] = df['date'].dt.to_period('M')
    
    # Calculate monthly statistics
    monthly = df.groupby('year_month').agg({
        'steps': 'mean',
        'distance': 'mean',
        'calories': 'mean'
    }).reset_index()
    
    monthly['year_month_str'] = monthly['year_month'].astype(str)
    
    # Create figure with subplots
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle('Data Langkah Kaki Bulanan (Monthly Steps Data)', fontsize=16, fontweight='bold')
    
    # Plot steps
    axes[0].bar(monthly['year_month_str'], monthly['steps'], color='skyblue', alpha=0.8)
    axes[0].set_ylabel('Langkah/Steps (rata-rata/average)', fontsize=11)
    axes[0].set_title('Rata-rata Langkah per Hari (Average Steps per Day)', fontsize=12)
    axes[0].grid(axis='y', alpha=0.3)
    axes[0].tick_params(axis='x', rotation=45)
    
    # Plot distance
    axes[1].bar(monthly['year_month_str'], monthly['distance'], color='lightcoral', alpha=0.8)
    axes[1].set_ylabel('Jarak/Distance (meter)', fontsize=11)
    axes[1].set_title('Rata-rata Jarak per Hari (Average Distance per Day)', fontsize=12)
    axes[1].grid(axis='y', alpha=0.3)
    axes[1].tick_params(axis='x', rotation=45)
    
    # Plot calories
    axes[2].bar(monthly['year_month_str'], monthly['calories'], color='lightgreen', alpha=0.8)
    axes[2].set_ylabel('Kalori/Calories (kcal)', fontsize=11)
    axes[2].set_xlabel('Bulan/Month', fontsize=11)
    axes[2].set_title('Rata-rata Kalori per Hari (Average Calories per Day)', fontsize=12)
    axes[2].grid(axis='y', alpha=0.3)
    axes[2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('activity_monthly_stats.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: activity_monthly_stats.png")
    
    # Print monthly statistics table
    print("\n" + "="*80)
    print("STATISTIK BULANAN LANGKAH KAKI (Monthly Activity Statistics)")
    print("="*80)
    print(f"{'Bulan/Month':<15} {'Steps (avg)':<15} {'Distance (m)':<15} {'Calories (kcal)':<15}")
    print("-"*80)
    for _, row in monthly.iterrows():
        print(f"{row['year_month_str']:<15} {row['steps']:<15.0f} {row['distance']:<15.0f} {row['calories']:<15.0f}")
    print("="*80)

def plot_sleep_data(df):
    """Plot sleep data analysis"""
    # Add year-month column
    df['year_month'] = df['date'].dt.to_period('M')
    
    # Calculate monthly sleep statistics
    monthly_sleep = df.groupby('year_month').agg({
        'deepSleepTime': 'mean',
        'shallowSleepTime': 'mean',
        'totalSleepTime': 'mean',
        'bedTime_hour': 'mean',
        'wakeTime_hour': 'mean'
    }).reset_index()
    
    monthly_sleep['year_month_str'] = monthly_sleep['year_month'].astype(str)
    
    # Create figure for sleep duration
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle('Data Waktu Tidur (Sleep Data)', fontsize=16, fontweight='bold')
    
    # Plot 1: Stacked bar chart for sleep components
    x = np.arange(len(monthly_sleep))
    width = 0.6
    
    axes[0].bar(x, monthly_sleep['deepSleepTime'], width, 
               label='Deep Sleep', color='#1f77b4', alpha=0.8)
    axes[0].bar(x, monthly_sleep['shallowSleepTime'], width,
               bottom=monthly_sleep['deepSleepTime'],
               label='Shallow Sleep', color='#ff7f0e', alpha=0.8)
    
    axes[0].set_ylabel('Waktu (menit)', fontsize=11)
    axes[0].set_title('Rata-rata Durasi Tidur per Bulan (Average Sleep Duration per Month)', fontsize=12)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(monthly_sleep['year_month_str'], rotation=45)
    axes[0].legend()
    axes[0].grid(axis='y', alpha=0.3)
    
    # Plot 2: Total sleep time line plot
    axes[1].plot(monthly_sleep['year_month_str'], monthly_sleep['totalSleepTime']/60,
                marker='o', linewidth=2, markersize=8, color='purple')
    axes[1].axhline(y=6, color='green', linestyle='--', alpha=0.5, label='6 hours (min)')
    axes[1].axhline(y=9, color='red', linestyle='--', alpha=0.5, label='9 hours (max)')
    axes[1].set_ylabel('Waktu Tidur Total (jam)', fontsize=11)
    axes[1].set_xlabel('Bulan/Month', fontsize=11)
    axes[1].set_title('Total Waktu Tidur per Malam (Total Sleep Time per Night)', fontsize=12)
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('sleep_duration_monthly.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: sleep_duration_monthly.png")
    
    # Plot sleep and wake times
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x = np.arange(len(monthly_sleep))
    width = 0.35
    
    ax.bar(x - width/2, monthly_sleep['bedTime_hour'], width,
          label='Jam Tidur (Bed Time)', color='navy', alpha=0.7)
    ax.bar(x + width/2, monthly_sleep['wakeTime_hour'], width,
          label='Jam Bangun (Wake Time)', color='orange', alpha=0.7)
    
    ax.set_ylabel('Jam (Hour)', fontsize=11)
    ax.set_xlabel('Bulan/Month', fontsize=11)
    ax.set_title('Rata-rata Jam Tidur dan Bangun (Average Bed Time and Wake Time)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(monthly_sleep['year_month_str'], rotation=45)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sleep_wake_times.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: sleep_wake_times.png")
    
    # Print sleep statistics table
    print("\n" + "="*100)
    print("STATISTIK BULANAN WAKTU TIDUR (Monthly Sleep Statistics)")
    print("="*100)
    print(f"{'Bulan':<12} {'Deep (min)':<12} {'Shallow (min)':<15} {'Total (min)':<12} {'Total (jam)':<12} {'Bed Time':<12} {'Wake Time':<12}")
    print("-"*100)
    for _, row in monthly_sleep.iterrows():
        bed_time = f"{int(row['bedTime_hour']):02d}:{int((row['bedTime_hour']%1)*60):02d}"
        wake_time = f"{int(row['wakeTime_hour']):02d}:{int((row['wakeTime_hour']%1)*60):02d}"
        print(f"{row['year_month_str']:<12} {row['deepSleepTime']:<12.0f} {row['shallowSleepTime']:<15.0f} "
              f"{row['totalSleepTime']:<12.0f} {row['totalSleepTime']/60:<12.1f} {bed_time:<12} {wake_time:<12}")
    print("="*100)

def plot_heartrate_data(df):
    """Plot heart rate analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Data Detak Jantung (Heart Rate Data)', fontsize=16, fontweight='bold')
    
    # 1. Histogram
    axes[0, 0].hist(df['heartRate'], bins=50, color='red', alpha=0.7, edgecolor='black')
    axes[0, 0].axvline(df['heartRate'].mean(), color='blue', linestyle='--', linewidth=2, label=f'Mean: {df["heartRate"].mean():.1f}')
    axes[0, 0].axvline(df['heartRate'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["heartRate"].median():.1f}')
    axes[0, 0].set_xlabel('Detak Jantung (BPM)', fontsize=11)
    axes[0, 0].set_ylabel('Frekuensi', fontsize=11)
    axes[0, 0].set_title('Distribusi Detak Jantung', fontsize=12)
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)
    
    # 2. Box plot
    axes[0, 1].boxplot(df['heartRate'], vert=True, patch_artist=True,
                       boxprops=dict(facecolor='lightcoral', alpha=0.7),
                       medianprops=dict(color='red', linewidth=2))
    axes[0, 1].set_ylabel('Detak Jantung (BPM)', fontsize=11)
    axes[0, 1].set_title('Box Plot Detak Jantung', fontsize=12)
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # 3. Time series
    df_sorted = df.sort_values('time')
    axes[1, 0].plot(df_sorted['time'], df_sorted['heartRate'], 
                   linewidth=0.5, alpha=0.5, color='darkred')
    axes[1, 0].set_xlabel('Waktu/Time', fontsize=11)
    axes[1, 0].set_ylabel('Detak Jantung (BPM)', fontsize=11)
    axes[1, 0].set_title('Detak Jantung dari Waktu ke Waktu', fontsize=12)
    axes[1, 0].grid(alpha=0.3)
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 4. Statistics text
    stats_text = f"""
    STATISTIK DETAK JANTUNG
    ========================
    Mean:              {df['heartRate'].mean():.2f} BPM
    Std Dev:           {df['heartRate'].std():.2f} BPM
    Median:            {df['heartRate'].median():.2f} BPM
    Mode:              {df['heartRate'].mode().iloc[0]:.0f} BPM
    Min:               {df['heartRate'].min():.0f} BPM
    Max:               {df['heartRate'].max():.0f} BPM
    Q1 (25%):          {df['heartRate'].quantile(0.25):.2f} BPM
    Q3 (75%):          {df['heartRate'].quantile(0.75):.2f} BPM
    Range:             {df['heartRate'].max() - df['heartRate'].min():.0f} BPM
    Count:             {len(df):,} measurements
    """
    axes[1, 1].text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                   verticalalignment='center', transform=axes[1, 1].transAxes)
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('heartrate_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: heartrate_analysis.png")
    
    # Print detailed statistics
    print("\n" + "="*80)
    print("STATISTIK DETAK JANTUNG (Heart Rate Statistics)")
    print("="*80)
    print(f"Mean:              {df['heartRate'].mean():.4f} BPM")
    print(f"Standard Error:    {df['heartRate'].sem():.4f} BPM")
    print(f"Mode:              {df['heartRate'].mode().iloc[0]:.0f} BPM")
    print(f"Median:            {df['heartRate'].median():.2f} BPM")
    print(f"First Quartile:    {df['heartRate'].quantile(0.25):.2f} BPM")
    print(f"Third Quartile:    {df['heartRate'].quantile(0.75):.2f} BPM")
    print(f"Variance:          {df['heartRate'].var():.4f}")
    print(f"Standard Deviation:{df['heartRate'].std():.4f} BPM")
    print(f"Kurtosis:          {df['heartRate'].kurtosis():.4f}")
    print(f"Skewness:          {df['heartRate'].skew():.4f}")
    print(f"Range:             {df['heartRate'].max() - df['heartRate'].min():.0f} BPM")
    print(f"Minimum:           {df['heartRate'].min():.0f} BPM")
    print(f"Maximum:           {df['heartRate'].max():.0f} BPM")
    print(f"Sum:               {df['heartRate'].sum():.0f}")
    print(f"Count:             {len(df):,}")
    print("="*80)

def main():
    """Main analysis function"""
    print("="*80)
    print("ANALISIS DATA KESEHATAN AMAZFIT BAND 3")
    print("Health Data Analysis - Walking Steps, Sleep, and Heart Rate")
    print("="*80)
    print()
    
    # Load and analyze activity data
    print("1. Loading Activity Data...")
    activity_df = load_activity_data()
    print(f"   → Loaded {len(activity_df)} days of activity data")
    print(f"   → Date range: {activity_df['date'].min().date()} to {activity_df['date'].max().date()}")
    plot_activity_monthly(activity_df)
    
    print()
    
    # Load and analyze sleep data
    print("2. Loading Sleep Data...")
    sleep_df = load_sleep_data()
    print(f"   → Loaded {len(sleep_df)} nights of sleep data")
    print(f"   → Date range: {sleep_df['date'].min().date()} to {sleep_df['date'].max().date()}")
    plot_sleep_data(sleep_df)
    
    print()
    
    # Load and analyze heart rate data
    print("3. Loading Heart Rate Data...")
    heartrate_df = load_heartrate_data()
    print(f"   → Loaded {len(heartrate_df)} heart rate measurements")
    print(f"   → Date range: {heartrate_df['time'].min().date()} to {heartrate_df['time'].max().date()}")
    plot_heartrate_data(heartrate_df)
    
    print()
    print("="*80)
    print("ANALISIS SELESAI! (Analysis Complete!)")
    print("Generated files:")
    print("  - activity_monthly_stats.png")
    print("  - sleep_duration_monthly.png")
    print("  - sleep_wake_times.png")
    print("  - heartrate_analysis.png")
    print("="*80)

if __name__ == "__main__":
    main()
