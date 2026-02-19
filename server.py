from mcp.server.fastmcp import FastMCP
from db import (get_hotels_by_location, book_room_db, cancel_booking_db,init_db,seed_hotels)


#server2


mcp = FastMCP("Hotel_Management_System")

init_db()
seed_hotels()

@mcp.tool("get_hotels_by_location")
def get_hotels_by_location_route(location:str):
    """fetch hotels by locatiion"""
    hotels=get_hotels_by_location(location)
    
    if hotels:
        return {"status":"success","data":hotels}
    else:
        return {"status":"error","message":"No hotels found in the specified location."}



@mcp.tool("book_room")
def Book_room_hotel_route(hotel_name:str,room_type:str,check_in:str,check_out:str):
    """book room in hotel"""
    booking_id=book_room_db(hotel_name,room_type,check_in,check_out)
    
    if booking_id:
        return {"status":"success","booking_id":booking_id}
    else:
        return {"status":"error","message":"Room not available or booking failed."}
        
        
@mcp.tool("cancel_booking")
def cancel_booking(booking_id:str):
    """cancel booking"""
    success=cancel_booking_db(booking_id)
    
    if success=="NOT_FOUND":
        return {"status":"error","message":"Booking Not found"}
    
    elif success=="ALREADY_CANCELLED":
        return {"status":"error","message":"already cancelled, o need to cancel again"}
    else:
        return {"status":"success","message":"booking cancelled successfully"}
    

if __name__ == "__main__":
    mcp.run(transport="stdio")