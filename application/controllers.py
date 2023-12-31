from flask import Flask, request,redirect,url_for,session
from flask import render_template
from flask import current_app as app
from application.database import db
from flask_sqlalchemy import SQLAlchemy
from application.models import *
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



@app.route("/",methods=["GET","POST"])
def index():
    venue=Venue.query.all()
    if "username" in session and session["user_role"]=='admin':
         return (render_template("admin.html",user=session["username"],role=session["user_role"]))
    elif  "username" in session:

        return render_template("index.html", user = session["username"], signed=True,role=session["user_role"],venue=venue)
    else:
        return render_template("index.html", user = "", signed=False,venue=venue)



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
      if "username" in session:
         return(redirect(url_for("index")))
      error_message=request.args.get("error")  
      return (render_template("login.html",error_message=error_message))
    else:
     if request.method=="POST":
        user=User.query.filter_by(email=request.form["email"]).first()
   
        if user:
            if bcrypt.check_password_hash(user.password,request.form["password"]):
                session["username"]= user.username
                session["user_role"]=user.roles[0].name
                session["user_email"]=user.email
                return redirect(url_for('index'))
            else:
              error_message = "Invalid email or password."
              return render_template('login.html', error_message=error_message)
      



@app.route("/register",methods=["GET","POST"])
def register():
    if "username" in session:
         return(redirect(url_for("index")))
    if request.method=='GET':
     return (render_template("register_user.html"))
    elif request.method=='POST':
        username=request.form["username"]
        email = request.form["email"]
        if "@" in email:
            user=User.query.filter_by(email=request.form["email"]).first()
            password=request.form["password"]
            if user:
               error="Email already registered"
               return (render_template("register_user.html", error=error))
            else:
               if(password!=request.form["confirm_password"]):
                  error="Password does not match with Confirm Password"
                  return(render_template("register_user.html",error=error))
               password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
              
               role = Role.query.filter_by(id=request.form['options']).first()
               
               user=User(username=username,email=email,password=password_hash)
               user.roles.append(role)
               user.tickets=[]
               db.session.add(user)
               db.session.commit()
               session["username"]=username  #maintaining cookie
               session["user_role"]=role.name
               session["user_email"]=user.email
               return redirect(url_for("login"))
        else:
           error = "Enter a valid email"
           return render_template("register_user.html", error = error)
        
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
        session.pop("user_role")
        session.pop("user_email")
    return redirect("/")




@app.route("/venue",methods=["GET","POST"])
def venue():
   if request.method=="GET":
      event=Event.query.all()
  
      return (render_template("venue.html",event=event))
   elif (request.method=="POST"):
     if "username" in session and session["user_role"]=='admin':
      form=request.form
      venue=Venue(name=form["name"],location=form["location"],capacity=form["capacity"])
      c=request.form.getlist('event')
      e=Event.query.all()
  
      for i in range(len(c)):
         for j in range(len(e)):  
           if c[i]==e[j].name:
            b=e[j]
            venue.events.append(b)
           
           else:
            continue
      db.session.add(venue)
      db.session.commit()
      venue.update_capacity_in_venue_event()
      return(redirect(url_for('event')))
     else:
              error="You are not an admin"
              return redirect(url_for('login',error=error))
   


@app.route("/event",methods=["GET","POST"])
def event():
   if request.method=="GET":
      venue=Venue.query.all()
      return (render_template("event.html",venue=venue))
   elif (request.method=="POST"):
     if "username" in session and session["user_role"]=='admin':
       form=request.form
       event=Event(name=form["name"],price=(form["price"]),duration=(form["duration"]))
       c=request.form.getlist('venue')
       v=Venue.query.all()
       print(c)
       for i in range(len(c)):
         for j in range(len(v)):  
           if c[i]==v[j].name:
            b=v[j]
            event.venues.append(b)
           
           else:
            continue
       db.session.add(event)
       db.session.commit()
       event.update_capacity_in_venue_event()
       return(redirect(url_for('venue')))
       
     else:   
              error="You are not an admin"
              return redirect(url_for('login',error=error))
   

@app.route("/delete_venue",methods=["GET","POST"])
def delete_venue():
      if request.method=="GET":
         venue=Venue.query.all()
          
         return render_template("delete_venue.html",venue=venue)
      elif (request.method=="POST"):
         if "username" in session and session["user_role"]=='admin':
             c=request.form.getlist('venue')
             v=Venue.query.all()
             event=Event.query.all()
             for i in range(len(c)):
               for j in range(len(v)):  
                if c[i]==v[j].name:
                  b=v[j]
                  for k in range (len(event)):
                   if b in event[k].venues:
                       event[k].venues.remove(b)
                  db.session.delete(b)
                  db.session.commit()
             return (redirect(url_for('venue')))
         else:
                    error="You are not an admin"
                    return redirect(url_for('login',error=error))
   
            
       
             

@app.route("/delete_event",methods=["GET","POST"])
def delete_event():
      if request.method=="GET":
         event=Event.query.all()
         return render_template("delete_event.html",events=event)
      elif (request.method=="POST"):
         if "username" in session and session["user_role"]=='admin':
             c=request.form.getlist('event')
             e=Event.query.all()
             
             venue=Venue.query.all()
            
             for i in range(len(c)):
               for j in range(len(e)):  
                if c[i]==e[j].name:
                  b=e[j]
                  b.venues.clear()
                  db.session.delete(b)
                  db.session.commit()
             return(redirect(url_for('event')))  
         else:
              error="You are not an admin"
              return redirect(url_for('login',error=error))
   

@app.route("/update_venue",methods=["GET","POST"])
def update_venue():
    if request.method=="GET":
         venue=Venue.query.all()
         event=Event.query.all()
         return render_template("update_venue.html",venue=venue,events=event)
    elif request.method=="POST":
      if "username" in session and session["user_role"]=="admin":
        venue=Venue.query.get(int(request.form['venue_id']))
        venue.name = request.form["name"]
        venue.location = request.form["location"]
        venue.capacity = request.form["capacity"]
        venue.events=[]
        c=request.form.getlist('event')
        e=Event.query.all()
        for i in range(len(c)):
         for j in range(len(e)):  
           if c[i]==e[j].name:
            b=e[j]
            venue.events.append(b)
           
           else:
            continue
        db.session.commit()
        venue.update_capacity_in_venue_event()
        return(redirect("/"))
      else:
              error="You are not an admin"
              return redirect(url_for('login',error=error))
   

       
@app.route("/update_event",methods=["GET","POST"])
def update_event():
      if request.method=="GET":
         venue=Venue.query.all()
         event=Event.query.all()
         return render_template("update_event.html",venue=venue,events=event)
      elif(request.method=="POST"):
       if "username" in session and session["user_role"]=='admin':
        event=Event.query.get(int(request.form['event_id']))
        event.name = request.form["name"]
        event.price = request.form["price"]
        event.duration = request.form["duration"]
        event.venues=[]
        c=request.form.getlist('venue')
        v=Venue.query.all()
        for i in range(len(c)):
         for j in range(len(v)):  
           if c[i]==v[j].name:
            b=v[j]
            event.venues.append(b)
           
           else:
            continue
        db.session.commit()
        event.update_capacity_in_venue_event()
        return(redirect("/"))
       else:
              error="You are not an admin"
              return redirect(url_for('login',error=error))
   
   
      



'''@app.route("/book_venue",methods=["GET","POST"])
def book_venue():
   if request.method=="GET":
      venues=Venue.query.all()

      return (render_template("book_venue.html",venue=venues))

@app.route("/book_venue/<int:venue_id>",methods=["GET","POST"])
def book_venue(venue_id):
   if request.method=="GET":
      venues=Venue.query.get(venue_id)

      return (render_template("book_venue.html",venue=venues))'''

@app.route("/book_venue", methods=["GET", "POST"])
@app.route("/book_venue/<int:venue_id>", methods=["GET", "POST"])
def book_venue(venue_id=None):
    if request.method == "GET":
        if venue_id is not None:
            # If venue_id is provided, query the specific venue
            venue = Venue.query.get(venue_id)
         
            return render_template("book_venue.html", venues=[venue])
        else:
            # If venue_id is not provided, retrieve all venues
            venues = Venue.query.all()
            return render_template("book_venue.html", venues=venues)


@app.route("/book_event",methods=["GET","POST"])
@app.route("/book_event/<int:event_id>", methods=["GET", "POST"])
def book_event(event_id=None):
   if request.method == "GET":
        if event_id is not None:
            # If venue_id is provided, query the specific venue
            event = Event.query.get(event_id)
         
            return render_template("book_event.html", event=[event])
        else:
            # If venue_id is not provided, retrieve all venues
            events = Event.query.all()
            return render_template("book_event.html", event=events)
   
@app.route("/book/<int:id>/<int:venue_id>",methods=["GET","POST"])
def book(id,venue_id):
   event=Event.query.get(id)
   v_e = Venue_Event.query.filter_by(v_id=venue_id, e_id=id).first() 
   if request.method=="GET":
      return (render_template("book.html",event=event,v_e=v_e))
   else:
      if request.method=="POST":
       
       if "username" not in session:
              return redirect(url_for('login'))
       if "username" in session and session["user_role"]!='admin':
             if v_e.capacity>0:
                form=request.form
                if v_e.capacity-int(form['tickets'])<0:
                  error="Sorry,only "+str(v_e.capacity)+" seats are left"
                  return (render_template("book.html",error=error,event=event,v_e=v_e))
                else:
                  v_e.capacity-=int(form['tickets'])
                  user=User.query.filter_by(email=session["user_email"]).first()
             
                  user.tickets.append(v_e)
                  db.session.commit()
                  user_ticket=User_Ticket_1.query.filter_by(user_id=user.id,ve_id=v_e.ve_id).first()
                  user_ticket.tickets=int(form['tickets'])
                  db.session.commit()
                  return redirect(url_for("order_summary", user_ticket_id=user_ticket.ut_id))
         
             else:
               error="Sorry all tickets sold ,please look for another venue"
               return (render_template("book.html",error=error,event=event,v_e=v_e))
      
       else:
             error="Only users can book tickets for an event"
             return (render_template("admin.html",user=session["username"],role=session["user_role"],error=error))

    
@app.route("/order_summary", methods=["GET"])
def order_summary():
    if "username" not in session:
        return redirect(url_for("login"))  # Redirect to login if user is not logged in

    user_ticket_id = request.args.get("user_ticket_id")
    user_ticket = User_Ticket_1.query.get(user_ticket_id)
    user=User.query.get(user_ticket.user_id)
    v_e=Venue_Event.query.get(user_ticket.ve_id)
    event=Event.query.get(v_e.e_id)
    venue=Venue.query.get(v_e.v_id)
    return render_template("summary.html", user_ticket=user_ticket,event=event,venue=venue,user=user)

@app.route("/display_user_tickets", methods=["GET"])
def display_user_tickets():
    if "user_email" not in session:
        return redirect(url_for("login"))  

    user = User.query.filter_by(email=session["user_email"]).first()
    
    user_tickets = User_Ticket_1.query.filter_by(user_id=user.id).all()
    ve=Venue_Event.query.all()
    venue=Venue.query.all()
    event=Event.query.all()


    return render_template("display.html", user_tickets=user_tickets,ve=ve,event=event,venue=venue)




@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "POST":
        query = request.form.get('query')
     
        if query:
            match_venues = Venue.query.filter(Venue.name.ilike(f"%{query}%")).all()
            match_events = Event.query.filter(Event.name.ilike(f"%{query}%")).all()
          
            return render_template("index.html", match_events=match_events,match_venues=match_venues)

    return render_template("index.html")



 
  

      
   






    
       
