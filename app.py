import streamlit as st
from database import get_connection

st.set_page_config(
    page_title="SkyTrack",
    page_icon="✈️",
    layout="wide"
)

# ----------------------------
# Custom Styling
# ----------------------------
st.markdown(
    """
    <style>
        .main {
            background-color: #f7f9fc;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        .hero {
            background: linear-gradient(135deg, #0f2747, #1d5c96);
            padding: 30px;
            border-radius: 18px;
            color: white;
            margin-bottom: 24px;
        }

        .hero h1 {
            margin: 0;
            font-size: 42px;
        }

        .hero p {
            margin-top: 8px;
            font-size: 18px;
            opacity: 0.9;
        }

        div.stButton > button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.55rem 1.2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Hero Header
# ----------------------------
st.markdown(
    """
    <div class="hero">
        <h1>✈️ SkyTrack</h1>
        <p>Airline Reservation and Flight Management System</p>
        <p style="font-size:15px;">
            Search flights, check seat availability, create bookings,
            and manage reservations using a MySQL relational database.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Database Status
# ----------------------------
try:
    conn = get_connection()
    conn.close()
    st.success("MySQL database connected successfully.")
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# ----------------------------
# Load Flights
# ----------------------------
try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            f.FlightID,
            f.FlightNumber,
            da.AirportCode AS FromAirport,
            aa.AirportCode AS ToAirport,
            f.DepartureTime,
            f.ArrivalTime,
            f.FlightStatus
        FROM Flight f
        JOIN Airport da
            ON f.DepartureAirportID = da.AirportID
        JOIN Airport aa
            ON f.ArrivalAirportID = aa.AirportID
        ORDER BY f.DepartureTime
    """)

    flights = cursor.fetchall()

    cursor.close()
    conn.close()

except Exception as e:
    st.error(f"Could not load flights: {e}")
    st.stop()

# ----------------------------
# Flight Search
# ----------------------------
st.markdown("## 🔎 Find a Flight")

airport_options = sorted(
    list(
        set(
            [flight["FromAirport"] for flight in flights]
            + [flight["ToAirport"] for flight in flights]
        )
    )
)

col1, col2 = st.columns(2)

with col1:
    from_airport = st.selectbox(
        "Departure Airport",
        airport_options
    )

with col2:
    to_airport = st.selectbox(
        "Arrival Airport",
        airport_options
    )

filtered_flights = [
    flight
    for flight in flights
    if flight["FromAirport"] == from_airport
    and flight["ToAirport"] == to_airport
]

if filtered_flights:

    st.success(f"{len(filtered_flights)} flight(s) found")

    st.dataframe(
        filtered_flights,
        use_container_width=True,
        hide_index=True
    )

    # If multiple flights exist for the same route,
    # allow the user to choose one.
    if len(filtered_flights) > 1:
        flight_labels = [
            f'{flight["FlightNumber"]} • '
            f'{flight["DepartureTime"]}'
            for flight in filtered_flights
        ]

        selected_flight_label = st.selectbox(
            "Choose a Flight",
            flight_labels
        )

        selected_flight = filtered_flights[
            flight_labels.index(selected_flight_label)
        ]
    else:
        selected_flight = filtered_flights[0]

    # ----------------------------
    # Available Seats
    # ----------------------------
    st.markdown("## 💺 Available Seats")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.SeatID,
                s.SeatNumber,
                s.SeatClass,
                s.SeatStatus
            FROM Seat s
            WHERE s.FlightID = %s
              AND s.SeatStatus = 'Available'
              AND NOT EXISTS (
                    SELECT 1
                    FROM Reservation r
                    WHERE r.SeatID = s.SeatID
                      AND r.FlightID = s.FlightID
                      AND r.ReservationStatus = 'Confirmed'
              )
            ORDER BY s.SeatNumber
        """, (selected_flight["FlightID"],))

        available_seats = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"Could not load available seats: {e}")
        available_seats = []

    if available_seats:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Flight",
                selected_flight["FlightNumber"]
            )

        with col2:
            st.metric(
                "Available Seats",
                len(available_seats)
            )

        with col3:
            st.metric(
                "Status",
                selected_flight["FlightStatus"]
            )

        st.dataframe(
            available_seats,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------
        # Reservation Form
        # ----------------------------
        st.markdown("## 🎫 Make a Reservation")

        seat_labels = [
            f'{seat["SeatNumber"]} • {seat["SeatClass"]}'
            for seat in available_seats
        ]

        selected_seat_label = st.selectbox(
            "Choose a Seat",
            seat_labels
        )

        selected_seat = available_seats[
            seat_labels.index(selected_seat_label)
        ]

        form_col1, form_col2 = st.columns(2)

        with form_col1:
            passenger_id = st.number_input(
                "Passenger ID",
                min_value=1,
                step=1,
                value=1
            )

        with form_col2:
            total_amount = st.number_input(
                "Ticket Amount ($)",
                min_value=0.0,
                step=10.0,
                value=0.0,
                format="%.2f"
            )

        if st.button(
            "Confirm Reservation",
            use_container_width=True
        ):

            # Ticket amount validation
            if total_amount <= 0:
                st.error(
                    "Ticket amount must be greater than $0."
                )

            else:
                conn = None
                cursor = None

                try:
                    conn = get_connection()
                    cursor = conn.cursor()

                    # ----------------------------
                    # Validate Passenger
                    # ----------------------------
                    cursor.execute("""
                        SELECT PassengerID
                        FROM Passenger
                        WHERE PassengerID = %s
                    """, (passenger_id,))

                    passenger_exists = cursor.fetchone()

                    if not passenger_exists:
                        st.error(
                            f"Passenger ID {passenger_id} does not exist."
                        )

                    else:
                        # ----------------------------
                        # Check Seat Availability Again
                        # ----------------------------
                        cursor.execute("""
                            SELECT
                                SeatID,
                                FlightID,
                                SeatStatus
                            FROM Seat
                            WHERE SeatID = %s
                            FOR UPDATE
                        """, (
                            selected_seat["SeatID"],
                        ))

                        seat_record = cursor.fetchone()

                        if not seat_record:
                            st.error(
                                "Selected seat does not exist."
                            )

                        elif (
                            seat_record["FlightID"]
                            != selected_flight["FlightID"]
                        ):
                            st.error(
                                "Selected seat does not belong "
                                "to this flight."
                            )

                        elif (
                            seat_record["SeatStatus"]
                            != "Available"
                        ):
                            st.error(
                                "Selected seat is no longer available."
                            )

                        else:
                            # ----------------------------
                            # Prevent Double Booking
                            # ----------------------------
                            cursor.execute("""
                                SELECT ReservationID
                                FROM Reservation
                                WHERE FlightID = %s
                                  AND SeatID = %s
                                  AND ReservationStatus = 'Confirmed'
                                LIMIT 1
                            """, (
                                selected_flight["FlightID"],
                                selected_seat["SeatID"]
                            ))

                            existing_booking = cursor.fetchone()

                            if existing_booking:
                                st.error(
                                    "This seat is already booked. "
                                    "Please select another seat."
                                )

                            else:
                                # ----------------------------
                                # Create Reservation
                                # ----------------------------
                                cursor.execute("""
                                    INSERT INTO Reservation
                                    (
                                        PassengerID,
                                        FlightID,
                                        SeatID,
                                        ReservationStatus,
                                        TotalAmount
                                    )
                                    VALUES (
                                        %s,
                                        %s,
                                        %s,
                                        'Confirmed',
                                        %s
                                    )
                                """, (
                                    passenger_id,
                                    selected_flight["FlightID"],
                                    selected_seat["SeatID"],
                                    total_amount
                                ))

                                conn.commit()

                                st.success(
                                    f'Reservation confirmed for '
                                    f'{selected_flight["FlightNumber"]}, '
                                    f'Seat '
                                    f'{selected_seat["SeatNumber"]}, '
                                    f'Amount ${total_amount:.2f}.'
                                )

                                st.rerun()

                except Exception as e:

                    if conn:
                        conn.rollback()

                    st.error(
                        f"Reservation failed: {e}"
                    )

                finally:

                    if cursor:
                        cursor.close()

                    if conn:
                        conn.close()

    else:
        st.warning(
            "No available seats for this flight."
        )

else:
    st.warning(
        "No flights found for this route."
    )

# ----------------------------
# Manage Bookings
# ----------------------------
st.divider()
st.markdown("## 📋 Manage Bookings")

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.ReservationID,
            CONCAT(
                p.FirstName,
                ' ',
                p.LastName
            ) AS PassengerName,
            f.FlightNumber,
            s.SeatNumber,
            s.SeatClass,
            r.ReservationStatus,
            r.TotalAmount
        FROM Reservation r
        JOIN Passenger p
            ON r.PassengerID = p.PassengerID
        JOIN Flight f
            ON r.FlightID = f.FlightID
        JOIN Seat s
            ON r.SeatID = s.SeatID
        ORDER BY r.ReservationID DESC
    """)

    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    if bookings:

        st.dataframe(
            bookings,
            use_container_width=True,
            hide_index=True
        )

        active_bookings = [
            booking
            for booking in bookings
            if booking["ReservationStatus"] != "Cancelled"
        ]

        if active_bookings:

            booking_labels = [
                f'Booking #{booking["ReservationID"]} • '
                f'{booking["PassengerName"]} • '
                f'{booking["FlightNumber"]} • '
                f'Seat {booking["SeatNumber"]}'
                for booking in active_bookings
            ]

            selected_booking_label = st.selectbox(
                "Select a booking to cancel",
                booking_labels
            )

            selected_booking = active_bookings[
                booking_labels.index(
                    selected_booking_label
                )
            ]

            if st.button(
                "Cancel Reservation",
                use_container_width=True
            ):

                conn = None
                cursor = None

                try:
                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute("""
                        UPDATE Reservation
                        SET ReservationStatus = 'Cancelled'
                        WHERE ReservationID = %s
                          AND ReservationStatus != 'Cancelled'
                    """, (
                        selected_booking["ReservationID"],
                    ))

                    conn.commit()

                    st.success(
                        f'Booking '
                        f'#{selected_booking["ReservationID"]} '
                        f'cancelled successfully.'
                    )

                    st.rerun()

                except Exception as e:

                    if conn:
                        conn.rollback()

                    st.error(
                        f"Cancellation failed: {e}"
                    )

                finally:

                    if cursor:
                        cursor.close()

                    if conn:
                        conn.close()

        else:
            st.info(
                "No active bookings available to cancel."
            )

    else:
        st.info(
            "No bookings found."
        )

except Exception as e:
    st.error(
        f"Could not load bookings: {e}"
    )

# ----------------------------
# Footer
# ----------------------------
st.divider()

st.caption(
    "SkyTrack • CS457 Data Modeling and Implementation Techniques • "
    "MySQL + Python + Streamlit"
)