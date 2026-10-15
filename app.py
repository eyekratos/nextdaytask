import json
from pathlib import Path
from datetime import date, datetime, timedelta
import streamlit as st

st.set_page_config(page_title="NextDay — Plan Tonight. Win Tomorrow.", page_icon="🌙", layout="wide")

DATA_FILE = Path(__file__).with_name("planner_data.json")

def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def day_key(d):
    return d.isoformat()

def blank_day():
    return {"tasks": [], "reflection": "", "tomorrow_note": "", "win": ""}

data = load_data()
today = date.today()
today_key = day_key(today)
tomorrow_key = day_key(today + timedelta(days=1))
data.setdefault(today_key, blank_day())
data.setdefault(tomorrow_key, blank_day())

st.markdown("""
<style>
.block-container {padding-top: 1.6rem; max-width: 1150px;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#111827,#312e81); color: white; margin-bottom: 1rem;}
.hero h1 {margin:0; font-size:2.2rem;}
.hero p {margin:.4rem 0 0 0; color:#dbeafe;}
.metric-card {padding: 1rem; border:1px solid rgba(128,128,128,.25); border-radius:14px;}
.small-muted {opacity:.75; font-size:.9rem;}
</style>
<div class="hero">
  <h1>🌙 NextDay</h1>
  <p>Plan tonight. Show up tomorrow. Build momentum one day at a time.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🧭 Your day")
    selected_date = st.date_input("Open a date", value=today)
    selected_key = day_key(selected_date)
    data.setdefault(selected_key, blank_day())
    st.caption("Your tasks are saved in planner_data.json on this computer.")
    st.divider()
    st.subheader("🎯 Simple rules")
    st.write("• Pick 1 main win")
    st.write("• Keep the plan realistic")
    st.write("• Done is better than perfect")

day = data[selected_key]
tasks = day.get("tasks", [])
done_count = sum(1 for t in tasks if t.get("done"))
total_count = len(tasks)
completion = int(done_count / total_count * 100) if total_count else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Tasks planned", total_count)
c2.metric("Completed", done_count)
c3.metric("Progress", f"{completion}%")
c4.metric("Main win", "Set" if day.get("win") else "Not set")

st.progress(completion / 100 if total_count else 0)

tab_today, tab_plan, tab_review, tab_roadmap = st.tabs(["☀️ Today", "🌙 Plan the night before", "🪞 Daily review", "🗺️ My roadmap"])

with tab_today:
    st.subheader(f"Today's mission — {selected_date.strftime('%A, %d %B %Y')}")
    if day.get("win"):
        st.info(f"🏆 Main win: {day['win']}")
    if not tasks:
        st.write("No tasks yet. Add a few in **Plan the night before**.")
    else:
        for idx, task in enumerate(tasks):
            cols = st.columns([0.08, 0.58, 0.14, 0.12, 0.08])
            new_done = cols[0].checkbox("Done", value=task.get("done", False), key=f"done_{selected_key}_{idx}", label_visibility="collapsed")
            if new_done != task.get("done", False):
                task["done"] = new_done
                save_data(data)
                st.rerun()
            title_text = task.get("title", "Untitled task")
            if task.get("done"):
                cols[1].markdown(f"~~{title_text}~~")
            else:
                cols[1].markdown(f"**{title_text}**")
            cols[2].write(task.get("priority", "Medium"))
            mins = task.get("minutes", 25)
            cols[3].write(f"⏱️ {mins}m")
            if cols[4].button("🗑️", key=f"delete_{selected_key}_{idx}", help="Delete task"):
                day["tasks"].pop(idx)
                save_data(data)
                st.rerun()
        st.caption(f"Estimated focused work: {sum(int(t.get('minutes',25)) for t in tasks)} minutes. Add breaks between tasks.")
    st.divider()
    st.subheader("🧠 If you feel stuck")
    st.write("1. Choose the smallest next action.  2. Work for just 10 minutes.  3. Reassess after starting.")

with tab_plan:
    st.subheader("Make tomorrow easier tonight")
    st.caption("Select a date in the sidebar, then add the tasks you want to complete on that date.")
    with st.form(f"add_task_{selected_key}", clear_on_submit=True):
        title = st.text_input("Task", placeholder="e.g., Practice Premiere Pro for 30 minutes")
        col_a, col_b, col_c = st.columns(3)
        priority = col_a.selectbox("Priority", ["High", "Medium", "Low"], index=1)
        minutes = col_b.selectbox("Time estimate", [10, 15, 25, 30, 45, 60, 90, 120], index=3)
        category = col_c.selectbox("Category", ["Work", "Learning", "Health", "Money", "Personal", "Other"])
        submitted = st.form_submit_button("＋ Add task", use_container_width=True)
        if submitted:
            if title.strip():
                day["tasks"].append({
                    "title": title.strip(),
                    "priority": priority,
                    "minutes": int(minutes),
                    "category": category,
                    "done": False,
                    "created_at": datetime.now().isoformat(timespec="seconds")
                })
                save_data(data)
                st.success("Task added!")
                st.rerun()
            else:
                st.warning("Pehle task ka naam likh bhai.")

    st.markdown("#### 🏆 Pick your one main win")
    win_value = st.text_input("If only one thing gets done, what should it be?", value=day.get("win", ""), placeholder="The one result that would make the day feel successful")
    if st.button("Save main win", key=f"save_win_{selected_key}"):
        day["win"] = win_value.strip()
        save_data(data)
        st.success("Main win saved.")
        st.rerun()

    st.markdown("#### 📝 Notes for future-you")
    note_value = st.text_area("Anything you want to remember tomorrow?", value=day.get("tomorrow_note", ""), placeholder="Keep it simple. Start with the first task; don't wait to feel motivated.")
    if st.button("Save note", key=f"save_note_{selected_key}"):
        day["tomorrow_note"] = note_value
        save_data(data)
        st.success("Note saved.")
        st.rerun()

    if tasks:
        st.markdown("#### Your plan")
        for i, task in enumerate(tasks, 1):
            st.write(f"{i}. **{task['title']}** — {task['priority']} priority · {task['minutes']} min · {task.get('category','Other')}")

with tab_review:
    st.subheader("Close the day without judging yourself")
    st.caption("A tiny review helps you improve tomorrow's plan.")
    reflection = st.text_area("What went well or what got in the way?", value=day.get("reflection", ""), placeholder="One honest sentence is enough.")
    if st.button("Save reflection", key=f"save_reflection_{selected_key}"):
        day["reflection"] = reflection
        save_data(data)
        st.success("Reflection saved.")
    if total_count:
        st.write(f"Today you completed **{done_count} of {total_count}** tasks.")
        if completion == 100:
            st.success("Perfect follow-through. Celebrate the win.")
        elif completion >= 60:
            st.info("Good progress. Carry the unfinished tasks forward only if they still matter.")
        else:
            st.info("No guilt. Make tomorrow's plan smaller and clearer.")

with tab_roadmap:
    st.subheader("🗺️ Bigger goal → small daily steps")
    st.caption("Use this as a simple roadmap. Break a goal into milestones, then put the next action into your daily plan.")
    roadmap_file = Path(__file__).with_name("roadmap.json")
    try:
        roadmap = json.loads(roadmap_file.read_text(encoding="utf-8")) if roadmap_file.exists() else []
    except Exception:
        roadmap = []
    with st.form("roadmap_form", clear_on_submit=True):
        goal = st.text_input("Goal", placeholder="e.g., Build a design portfolio")
        milestone = st.text_input("Next milestone", placeholder="e.g., Finish 3 practice projects")
        action = st.text_input("Next small action", placeholder="e.g., Practice typography for 25 minutes")
        add_goal = st.form_submit_button("＋ Add roadmap step")
        if add_goal:
            if goal.strip() and action.strip():
                roadmap.append({"goal": goal.strip(), "milestone": milestone.strip(), "action": action.strip(), "done": False})
                roadmap_file.write_text(json.dumps(roadmap, ensure_ascii=False, indent=2), encoding="utf-8")
                st.rerun()
            else:
                st.warning("Goal aur next action dono likh.")
    if roadmap:
        for i, item in enumerate(roadmap):
            cols = st.columns([0.08, 0.32, 0.30, 0.30])
            checked = cols[0].checkbox("Done", value=item.get("done", False), key=f"roadmap_done_{i}", label_visibility="collapsed")
            if checked != item.get("done", False):
                item["done"] = checked
                roadmap_file.write_text(json.dumps(roadmap, ensure_ascii=False, indent=2), encoding="utf-8")
                st.rerun()
            cols[1].markdown(f"**{item['goal']}**")
            cols[2].write(item.get("milestone", "—"))
            cols[3].write(item["action"])
        if st.button("Clear completed roadmap steps"):
            roadmap = [x for x in roadmap if not x.get("done")]
            roadmap_file.write_text(json.dumps(roadmap, ensure_ascii=False, indent=2), encoding="utf-8")
            st.rerun()
    else:
        st.write("Your roadmap is empty. Add a goal and its next small action above.")

st.divider()
st.caption("NextDay is a simple personal planner. It stores data locally beside the app; back up planner_data.json and roadmap.json if your tasks matter.")
with st.expander("📦 Export or back up my plan"):
    st.download_button("Download daily planner data", data=json.dumps(data, ensure_ascii=False, indent=2), file_name="planner_backup.json", mime="application/json")
    if roadmap_file.exists():
        st.download_button("Download roadmap data", data=roadmap_file.read_bytes(), file_name="roadmap_backup.json", mime="application/json")
