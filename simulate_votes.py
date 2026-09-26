"""
Hostel Food Poll Voting Simulator
Simulates realistic student voting activity for live presentations and demonstrations.
Selects unvoted students from the hostel roster and casts randomized votes with realistic weighting.
"""

import random
import time
from database import get_active_polls, get_poll_by_id, get_admin_detailed_data, cast_vote

def run_simulation(num_votes=10, delay_seconds=0.2):
    active_polls = get_active_polls()
    if not active_polls:
        print("❌ No active polls found to simulate voting for. Please create one in the Cook Portal first!")
        return
        
    poll = get_poll_by_id(active_polls[0]['id'])
    poll_id = poll['id']
    dishes = poll['dishes']
    
    if not dishes:
        print(f"❌ Poll '{poll['title']}' has no dishes to vote on.")
        return
        
    admin_data = get_admin_detailed_data(poll_id)
    non_polled = admin_data['non_polled_students']
    
    if not non_polled:
        print(f"🎉 All {admin_data['total_hostel_students']} hostel students have already voted in this poll!")
        return
        
    students_to_vote = non_polled[:min(num_votes, len(non_polled))]
    
    print("=" * 65)
    print(f"🗳️  SIMULATING VOTING FOR: {poll['title']} ({poll_id})")
    print(f"👥  Available Non-Polled Students: {len(non_polled)}")
    print(f"🚀  Simulating {len(students_to_vote)} live student votes...")
    print("=" * 65)
    
    # Weighted preference: give higher weights to favorite dishes
    weights = [35, 25, 20, 20][:len(dishes)]
    if len(weights) < len(dishes):
        weights += [10] * (len(dishes) - len(weights))
        
    voted_count = 0
    for s in students_to_vote:
        chosen_dish = random.choices(dishes, weights=weights[:len(dishes)], k=1)[0]
        
        success, msg = cast_vote(poll_id, s['student_id'], chosen_dish['id'])
        if success:
            voted_count += 1
            print(f"  ✅ [{s['room_no']}] {s['name']:<18} voted for: {chosen_dish['name']}")
        else:
            print(f"  ⚠️ Could not cast vote for {s['name']}: {msg}")
            
        if delay_seconds > 0:
            time.sleep(delay_seconds)
            
    print("=" * 65)
    print(f"✨ Simulation Complete! {voted_count} student votes cast successfully.")
    
    updated_data = get_admin_detailed_data(poll_id)
    print(f"📊 New Turnout: {updated_data['polled_count']}/{updated_data['total_hostel_students']} students ({updated_data['turnout_pct']}%)")
    print(f"👑 Leading Dish: {updated_data['winner']}")
    print("=" * 65)
    print("You can now open Admin Portal or Cook Portal to see the updated graphs and tallies!")

if __name__ == "__main__":
    import sys
    count = 10
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        count = int(sys.argv[1])
    run_simulation(num_votes=count)
