import streamlit as st
from database import get_connection
from datetime import date

# -------------------------------------------------
# Automatic Flight Fares
# -------------------------------------------------
FLIGHT_FARES = {
    "ST101": 320.00,
    "ST202": 450.00,
    "ST303": 520.00,
    "ST404": 275.00,
    "ST505": 350.00
}

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="SkyTrack",
    page_icon="✈️",
    layout="wide"
)

# -------------------------------------------------
# Premium Colorful Styling
# -------------------------------------------------
st.markdown(
    """
    <style>

    /* Main Background */
    .stApp {
        background:
            radial-gradient(circle at top left, #eef6ff 0%, transparent 35%),
            radial-gradient(circle at top right, #f4edff 0%, transparent 35%),
            linear-gradient(180deg, #f8fbff 0%, #ffffff 45%, #f8fafc 100%);
    }

    .block-container {
        max-width: 1250px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Hero */
    .hero {
        background:
            linear-gradient(
                120deg,
                #0b1f3a 0%,
                #123b6d 35%,
                #1769aa 70%,
                #5b3cc4 100%
            );
        padding: 42px 46px;
        border-radius: 28px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 18px 45px rgba(30, 64, 175, 0.20);
        position: relative;
        overflow: hidden;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        right: -60px;
        top: -80px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
    }

    .hero h1 {
        margin: 0;
        font-size: 52px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .hero h3 {
        margin-top: 14px;
        margin-bottom: 6px;
        font-size: 23px;
        font-weight: 500;
        color: #e5efff;
    }

    .hero p {
        font-size: 16px;
        color: #dce9ff;
        margin-top: 10px;
        max-width: 800px;
    }

    /* Section Headings */
    h2 {
        color: #12213a;
        font-weight: 750 !important;
        margin-top: 25px !important;
    }

    /* Success / Info / Warning */
    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: none;
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.05);
    }

    /* Inputs */
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border: 1px solid #d8e1ec !important;
        background: white !important;
    }

    div[data-testid="stDateInput"] input,
    div[data-testid="stNumberInput"] input {
        border-radius: 12px !important;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        border: none;
        border-radius: 12px;
        padding: 0.72rem 1.2rem;
        font-weight: 700;
        font-size: 16px;
        color: white;
        background: linear-gradient(
            90deg,
            #2563eb,
            #4f46e5,
            #7c3aed
        );
        box-shadow: 0 8px 18px rgba(79, 70, 229, 0.20);
        transition: 0.2s ease-in-out;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 24px rgba(79, 70, 229, 0.28);
        color: white;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #ffffff,
            #f5f9ff
        );
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 7px 22px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #1d4ed8;
        font-weight: 800;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.07);
    }

    /* Custom Section Card */
    .info-card {
        background: linear-gradient(
            135deg,
            #eff6ff 0%,
            #eef2ff 55%,
            #faf5ff 100%
        );
        border: 1px solid #dbeafe;
        border-radius: 18px;
        padding: 22px;
        margin: 15px 0 18px 0;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.07);
    }

    .info-card-title {
        font-size: 15px;
        font-weight: 700;
        color: #334155;
        margin-bottom: 4px;
    }

    .info-card-value {
        font-size: 23px;
        font-weight: 800;
        color: #1d4ed8;
    }

    /* Footer */
    .footer-box {
        margin-top: 20px;
        text-align: center;
        padding: 18px;
        border-radius: 16px;
        color: #64748b;
        background: linear-gradient(
            90deg,
            #eff6ff,
            #f5f3ff,
            #ecfeff
        );
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Hero
# -------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>✈️ SkyTrack</h1>
        <h3>Airline Reservation & Flight Management System</h3>
        <p>
            Search flights by route and travel date, check real-time seat
            availability, create reservations, and manage bookings through
            a MySQL-powered cloud database.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Database Connection
# -------------------------------------------------
try:
    conn = get_connection()
    conn.close()
    st.success("✅ MySQL cloud database connected successfully.")
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# -------------------------------------------------
# Load Flights
# -------------------------------------------------
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

# -------------------------------------------------
# Flight Search
# -------------------------------------------------
st.markdown("## 🔍 Search Your Flight")

airport_options = sorted(
    list(
        set(
            [flight["FromAirport"] for flight in flights]
            + [flight["ToAirport"] for flight in flights]
        )
    )
)

search_col1, search_col2, search_col3 = st.columns(3)

with search_col1:
    from_airport = st.selectbox(
        "🛫 Departure Airport",
        airport_options
    )

with search_col2:
    to_airport = st.selectbox(
        "🛬 Arrival Airport",
        airport_options
    )

with search_col3:
    travel_date = st.date_input(
        "📅 Travel Date",
        value=date.today()
    )

filtered_flights = [
    flight
    for flight in flights
    if flight["FromAirport"] == from_airport
    and flight["ToAirport"] == to_airport
    and flight["DepartureTime"].date() == travel_date
]

# -------------------------------------------------
# Search Results
# -------------------------------------------------
if filtered_flights:

    st.success(
        f"✈️ {len(filtered_flights)} flight(s) found for "
        f"{from_airport} → {to_airport} on "
        f"{travel_date.strftime('%B %d, %Y')}."
    )

    flight_display = []

    for flight in filtered_flights:

        fare = FLIGHT_FARES.get(
            flight["FlightNumber"],
            0.00
        )

        flight_display.append(
            {
                "Flight": flight["FlightNumber"],
                "From": flight["FromAirport"],
                "To": flight["ToAirport"],
                "Departure": flight["DepartureTime"],
                "Arrival": flight["ArrivalTime"],
                "Status": flight["FlightStatus"],
                "Fare": f"${fare:.2f}"
            }
        )

    st.dataframe(
        flight_display,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------------------------------
    # Select Flight
    # -------------------------------------------------
    if len(filtered_flights) > 1:

        flight_labels = [
            f'{flight["FlightNumber"]} • '
            f'{flight["DepartureTime"].strftime("%I:%M %p")} • '
            f'${FLIGHT_FARES.get(flight["FlightNumber"], 0.00):.2f}'
            for flight in filtered_flights
        ]

        selected_flight_label = st.selectbox(
            "✈️ Choose a Flight",
            flight_labels
        )

        selected_flight = filtered_flights[
            flight_labels.index(selected_flight_label)
        ]

    else:
        selected_flight = filtered_flights[0]

    total_amount = FLIGHT_FARES.get(
        selected_flight["FlightNumber"],
        0.00
    )

    # -------------------------------------------------
    # Selected Flight Summary
    # -------------------------------------------------
    st.markdown("## 🌤️ Selected Flight")

    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

    with summary_col1:
        st.metric(
            "✈️ Flight",
            selected_flight["FlightNumber"]
        )

    with summary_col2:
        st.metric(
            "🕒 Departure",
            selected_flight["DepartureTime"].strftime("%I:%M %p")
        )

    with summary_col3:
        st.metric(
            "📡 Status",
            selected_flight["FlightStatus"]
        )

    with summary_col4:
        st.metric(
            "💵 Ticket Fare",
            f"${total_amount:.2f}"
        )

    # -------------------------------------------------
    # Available Seats
    # -------------------------------------------------
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
        """, (
            selected_flight["FlightID"],
        ))

        available_seats = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"Could not load available seats: {e}")
        available_seats = []

    if available_seats:

        st.success(
            f"🟢 {len(available_seats)} seat(s) currently available."
        )

        st.dataframe(
            available_seats,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # Reservation Form
        # -------------------------------------------------
        st.markdown("## 🎫 Make a Reservation")

        seat_labels = [
            f'{seat["SeatNumber"]} • {seat["SeatClass"]}'
            for seat in available_seats
        ]

        reserve_col1, reserve_col2 = st.columns(2)

        with reserve_col1:
            selected_seat_label = st.selectbox(
                "💺 Choose a Seat",
                seat_labels
            )

        selected_seat = available_seats[
            seat_labels.index(selected_seat_label)
        ]

        with reserve_col2:
            passenger_id = st.number_input(
                "👤 Passenger ID",
                min_value=1,
                step=1,
                value=1
            )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-title">
                    Booking Summary
                </div>
                <div class="info-card-value">
                    {selected_flight["FlightNumber"]}
                    &nbsp; • &nbsp;
                    {from_airport} → {to_airport}
                </div>
                <br>
                📅 {travel_date.strftime("%B %d, %Y")}
                &nbsp;&nbsp; | &nbsp;&nbsp;
                💺 Seat {selected_seat["SeatNumber"]}
                &nbsp;&nbsp; | &nbsp;&nbsp;
                💵 ${total_amount:.2f}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "✅ Confirm Reservation",
            use_container_width=True
        ):

            conn = None
            cursor = None

            try:
                conn = get_connection()
                cursor = conn.cursor()

                # Validate Passenger
                cursor.execute("""
                    SELECT PassengerID
                    FROM Passenger
                    WHERE PassengerID = %s
                """, (
                    passenger_id,
                ))

                passenger_exists = cursor.fetchone()

                if not passenger_exists:

                    st.error(
                        f"Passenger ID {passenger_id} does not exist."
                    )

                else:

                    # Recheck Seat
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
                            "Selected seat does not belong to this flight."
                        )

                    elif (
                        seat_record["SeatStatus"]
                        != "Available"
                    ):

                        st.error(
                            "Selected seat is no longer available."
                        )

                    else:

                        # Prevent Duplicate Booking
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
                                f'🎉 Reservation confirmed! '
                                f'Flight {selected_flight["FlightNumber"]}, '
                                f'Seat {selected_seat["SeatNumber"]}, '
                                f'Fare ${total_amount:.2f}.'
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
            "⚠️ No available seats for this flight."
        )

else:

    st.warning(
        f"⚠️ No flights available from {from_airport} "
        f"to {to_airport} on "
        f"{travel_date.strftime('%B %d, %Y')}."
    )

# -------------------------------------------------
# Manage Bookings
# -------------------------------------------------
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
            da.AirportCode AS FromAirport,
            aa.AirportCode AS ToAirport,
            f.DepartureTime,
            s.SeatNumber,
            s.SeatClass,
            r.ReservationStatus,
            r.TotalAmount
        FROM Reservation r
        JOIN Passenger p
            ON r.PassengerID = p.PassengerID
        JOIN Flight f
            ON r.FlightID = f.FlightID
        JOIN Airport da
            ON f.DepartureAirportID = da.AirportID
        JOIN Airport aa
            ON f.ArrivalAirportID = aa.AirportID
        JOIN Seat s
            ON r.SeatID = s.SeatID
        ORDER BY r.ReservationID DESC
    """)

    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    if bookings:

        booking_display = []

        for booking in bookings:

            booking_display.append(
                {
                    "Booking ID": booking["ReservationID"],
                    "Passenger": booking["PassengerName"],
                    "Flight": booking["FlightNumber"],
                    "Route": (
                        f'{booking["FromAirport"]} → '
                        f'{booking["ToAirport"]}'
                    ),
                    "Travel Date": (
                        booking["DepartureTime"].strftime(
                            "%Y-%m-%d"
                        )
                    ),
                    "Seat": booking["SeatNumber"],
                    "Class": booking["SeatClass"],
                    "Status": booking["ReservationStatus"],
                    "Amount": (
                        f'${float(booking["TotalAmount"]):.2f}'
                    )
                }
            )

        st.dataframe(
            booking_display,
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
                f'{booking["DepartureTime"].strftime("%Y-%m-%d")} • '
                f'Seat {booking["SeatNumber"]}'
                for booking in active_bookings
            ]

            selected_booking_label = st.selectbox(
                "🗂️ Select a booking to cancel",
                booking_labels
            )

            selected_booking = active_bookings[
                booking_labels.index(
                    selected_booking_label
                )
            ]

            if st.button(
                "❌ Cancel Reservation",
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
                        f'✅ Booking '
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

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.divider()

st.markdown(
    """
    <div class="footer-box">
        ✈️ <b>SkyTrack</b> &nbsp; • &nbsp;
        CS457 Data Modeling and Implementation Techniques
        &nbsp; • &nbsp;
        MySQL + Python + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)