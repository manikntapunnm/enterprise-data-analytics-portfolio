import pandas as pd
import random
from datetime import datetime, timedelta
import os

print("⏳ Generating corporate support infrastructure logs...")

ticket_categories = ['Login Issue', 'Payment Failure', 'Bug Report', 'Subscription Change', 'API Timeout']
priorities = ['P1-Critical', 'P2-High', 'P3-Medium', 'P4-Low']
statuses = ['Resolved', 'Closed', 'Escalated', 'Open']

support_data = []
base_date = datetime(2026, 1, 1)

for i in range(30000):
    ticket_id = f"TKT_{500000 + i}"
    created_time = base_date + timedelta(
        days=random.randint(0, 200), 
        hours=random.randint(0, 23), 
        minutes=random.randint(0, 59)
    )
    category = random.choice(ticket_categories)
    priority = random.choices(priorities, weights=[0.1, 0.2, 0.4, 0.3])[0]
    status = random.choices(statuses, weights=[0.5, 0.3, 0.1, 0.1])[0]
    
    # Simulate processing intervals based on target business priority rules
    if status in ['Resolved', 'Closed']:
        if priority == 'P1-Critical':
            resolution_hours = random.uniform(0.5, 4.0)
        elif priority == 'P2-High':
            resolution_hours = random.uniform(2.0, 12.0)
        else:
            resolution_hours = random.uniform(12.0, 72.0)
    else:
        resolution_hours = None
        
    # Check compliance rules (P1 must be cleared in <2hrs, P2 in <8hrs)
    is_sla_violated = 0
    if resolution_hours:
        if priority == 'P1-Critical' and resolution_hours > 2.0:
            is_sla_violated = 1
        elif priority == 'P2-High' and resolution_hours > 8.0:
            is_sla_violated = 1
            
    support_data.append([
        ticket_id, 
        created_time.strftime('%Y-%m-%d %H:%M:%S'), 
        category, 
        priority, 
        status, 
        round(resolution_hours, 2) if resolution_hours else None, 
        is_sla_violated
    ])

df_support = pd.DataFrame(
    support_data, 
    columns=['ticket_id', 'created_at', 'issue_category', 'priority_tier', 'status', 'resolution_hours', 'sla_violated_flag']
)

# Target export straight into the local project path
output_path = os.path.join(os.path.dirname(__file__), 'support_operations.csv')
df_support.to_csv(output_path, index=False)

print(f"✅ Success! Support Operations Dataset created at: {output_path}")