from app.database import get_recent_failed_events


def detect_systemic_failure():
    events = get_recent_failed_events(minutes=5)

    failure_count = len(events)

    unique_customers = {
         event["customer_email"]

         for event in events
    }

    customer_count = len(unique_customers)

    if failure_count >= 5 and customer_count >=3:
        return True
    
    return False