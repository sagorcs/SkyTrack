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
# Colorful Professional Styling
# -------------------------------------------------
st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(circle at top left, #e8f3ff 0%, transparent 32%),
            radial-gradient(circle at top right, #f1eaff 0%, transparent 32%),
            linear-gradient(180deg, #f8fbff 0%, #ffffff 50%, #f8fafc 100%);
    }

    .block-container {
        max-width: 1250px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

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
        width: 280px;
        height: 280px;
        right: -70px;
        top: -90px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
    }

    .hero h1 {
        margin: 0;
        font-size: 52px;
        font-weight: 800;
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
        max-width: 850px;
    }

    h2 {
        color: #12213a;
        font-weight: 750 !important;
        margin-top: 25px !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: none;
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.05);
    }

    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border: 1px solid #d8e1ec !important;
        background: white !important;
    }

    div[data-testid="stDateInput"] input,
    div[data-testid="stNumberInput"] input {
        border-radius: 12px !important;
    }

    div.stButton > button {
        width: 100%;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.2rem;
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
    }

    div.stButton > button:hover {
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 12px 24px rgba(79, 70, 229, 0.28);
    }

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

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.07);
    }

    .booking-card {
        background:
            linear-gradient(
                135deg,
                #eff6ff 0%,
                #eef2ff 45%,
                #faf5ff 100%
            );
        border: 1px solid #dbeafe;
        border-radius: 20px;
        padding: 24px;
        margin: 18px 0;
        box-shadow: 0 8px 22px rgba(59, 130, 246, 0.08);
    }

    .booking-title {
        color: #475569;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .booking-flight {
        color: #1d4ed8;
        font-size: 24px;
        font-weight: 800;
    }

    .total-fare {
        margin-top: 14px;
        padding: 12px 15px;
        background: white;
        border-radius: 12px;
        color: #0f766e;
        font-size: 19px;
        font-weight: 800;
        display: inline-block;
    }

    .footer-box {
        margin-top: 20px;
        text-align: center;
        padding: 18px;
        border-radius: 16px;
        color: #64748b;
        background:
            linear-gradient(
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
# Hero Section
# -------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>✈️ SkyTrack</h1>
        <h3>Airline Reservation & Flight Management System</h3>
        <p>
            Search flights by route and travel date, check seat availability,
            calculate fares automatically, create bookings, and manage
            reservations through a MySQL-powered cloud database.
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

    st.success(
        "✅ MySQL cloud database connected successfully."
    )

except Exception as e:

    st.error(
        f"Database connection failed: {e}"
    )

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

    st.error(
        f"Could not load flights: {e}"
    )

    st.stop()

# -------------------------------------------------
# Flight Search
# -------------------------------------------------
st.markdown("## 🔍 Search Your Flight")

airport_options = sorted(
    list(
        set(
            [flight["FromAirport"] for flight in flights]
            +
            [flight["ToAirport"] for flight in flights]
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

# -------------------------------------------------
# Filter Flights
# -------------------------------------------------
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
                "Fare / Passenger": f"${fare:.2f}"
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
            flight_labels.index(
                selected_flight_label
            )
        ]

    else:

        selected_flight = filtered_flights[0]

    base_fare = FLIGHT_FARES.get(
        selected_flight["FlightNumber"],
        0.00
    )

    # -------------------------------------------------
    # Flight Summary
    # -------------------------------------------------
    st.markdown("## 🌤️ Selected Flight")

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:

        st.metric(
            "✈️ Flight",
            selected_flight["FlightNumber"]
        )

    with metric2:

        st.metric(
            "🕒 Departure",
            selected_flight[
                "DepartureTime"
            ].strftime("%I:%M %p")
        )

    with metric3:

        st.metric(
            "📡 Status",
            selected_flight["FlightStatus"]
        )

    with metric4:

        st.metric(
            "💵 Fare / Passenger",
            f"${base_fare:.2f}"
        )

    # -------------------------------------------------
    # Load Available Seats
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
              )
            ORDER BY s.SeatNumber
        """, (
            selected_flight["FlightID"],
        ))

        available_seats = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:

        st.error(
            f"Could not load available seats: {e}"
        )

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

        form_col1, form_col2 = st.columns(2)

        with form_col1:

            passenger_id = st.number_input(
                "👤 Booking Passenger ID",
                min_value=1,
                step=1,
                value=1
            )

        with form_col2:

            passenger_count = st.number_input(
                "👥 Number of Passengers",
                min_value=1,
                max_value=10,
                step=1,
                value=1
            )

        # -------------------------------------------------
        # Seat Selection
        # -------------------------------------------------
        seat_lookup = {
            f'{seat["SeatNumber"]} • {seat["SeatClass"]}':
            seat
            for seat in available_seats
        }

        seat_labels = list(
            seat_lookup.keys()
        )

        selected_seat_labels = st.multiselect(
            "💺 Select Seat(s)",
            seat_labels,
            max_selections=int(passenger_count)
        )

        selected_seats = [
            seat_lookup[label]
            for label in selected_seat_labels
        ]

        # -------------------------------------------------
        # Fare Calculation
        # -------------------------------------------------
        total_amount = (
            base_fare
            *
            int(passenger_count)
        )

        seat_text = (
            ", ".join(
                seat["SeatNumber"]
                for seat in selected_seats
            )
            if selected_seats
            else "Not selected"
        )

        st.markdown(
            f"""
            <div class="booking-card">

                <div class="booking-title">
                    Booking Summary
                </div>

                <div class="booking-flight">
                    {selected_flight["FlightNumber"]}
                    &nbsp; • &nbsp;
                    {from_airport} → {to_airport}
                </div>

                <br>

                📅 <b>Travel Date:</b>
                {travel_date.strftime("%B %d, %Y")}

                <br><br>

                👥 <b>Passengers:</b>
                {passenger_count}

                <br><br>

                💺 <b>Selected Seats:</b>
                {seat_text}

                <br><br>

                💵 <b>Fare:</b>
                ${base_fare:.2f}
                ×
                {passenger_count}

                <br>

                <div class="total-fare">
                    Total Fare: ${total_amount:.2f}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # Confirm Reservation
        # -------------------------------------------------
        if st.button(
            "✅ Confirm Reservation",
            use_container_width=True
        ):

            # Require exact seat count
            if len(selected_seats) != int(
                passenger_count
            ):

                st.error(
                    f"Please select exactly "
                    f"{int(passenger_count)} seat(s) "
                    f"for {int(passenger_count)} passenger(s)."
                )

            elif base_fare <= 0:

                st.error(
                    "Fare is not configured for this flight."
                )

            else:

                conn = None
                cursor = None

                try:

                    conn = get_connection()
                    cursor = conn.cursor()

                    # -----------------------------------------
                    # Passenger Validation
                    # -----------------------------------------
                    cursor.execute("""
                        SELECT
                            PassengerID,
                            FirstName,
                            LastName
                        FROM Passenger
                        WHERE PassengerID = %s
                    """, (
                        passenger_id,
                    ))

                    passenger = cursor.fetchone()

                    if not passenger:

                        st.error(
                            f"Passenger ID "
                            f"{passenger_id} "
                            f"does not exist."
                        )

                    else:

                        booking_successful = True

                        # -----------------------------------------
                        # Recheck all selected seats
                        # -----------------------------------------
                        for seat in selected_seats:

                            cursor.execute("""
                                SELECT
                                    SeatID,
                                    FlightID,
                                    SeatStatus
                                FROM Seat
                                WHERE SeatID = %s
                                FOR UPDATE
                            """, (
                                seat["SeatID"],
                            ))

                            current_seat = (
                                cursor.fetchone()
                            )

                            if not current_seat:

                                booking_successful = False

                                st.error(
                                    f'Seat '
                                    f'{seat["SeatNumber"]} '
                                    f'does not exist.'
                                )

                                break

                            if (
                                current_seat["FlightID"]
                                !=
                                selected_flight["FlightID"]
                            ):

                                booking_successful = False

                                st.error(
                                    f'Seat '
                                    f'{seat["SeatNumber"]} '
                                    f'does not belong '
                                    f'to this flight.'
                                )

                                break

                            if (
                                current_seat["SeatStatus"]
                                !=
                                "Available"
                            ):

                                booking_successful = False

                                st.error(
                                    f'Seat '
                                    f'{seat["SeatNumber"]} '
                                    f'is no longer available.'
                                )

                                break

                            cursor.execute("""
                                SELECT ReservationID
                                FROM Reservation
                                WHERE FlightID = %s
                                  AND SeatID = %s
                                LIMIT 1
                            """, (
                                selected_flight[
                                    "FlightID"
                                ],
                                seat["SeatID"]
                            ))

                            old_booking = (
                                cursor.fetchone()
                            )

                            if old_booking:

                                booking_successful = False

                                st.error(
                                    f'Seat '
                                    f'{seat["SeatNumber"]} '
                                    f'has already been used '
                                    f'in another reservation.'
                                )

                                break

                        # -----------------------------------------
                        # Insert Reservations
                        # -----------------------------------------
                        if booking_successful:

                            for seat in selected_seats:

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
                                    selected_flight[
                                        "FlightID"
                                    ],
                                    seat["SeatID"],
                                    base_fare
                                ))

                            conn.commit()

                            st.success(
                                f"🎉 Booking confirmed for "
                                f"{int(passenger_count)} "
                                f"passenger(s)! "
                                f"Total Fare: "
                                f"${total_amount:.2f}"
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
        f"⚠️ No flights available from "
        f"{from_airport} to {to_airport} "
        f"on "
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
                    "Booking ID":
                        booking["ReservationID"],

                    "Passenger":
                        booking["PassengerName"],

                    "Flight":
                        booking["FlightNumber"],

                    "Route":
                        (
                            f'{booking["FromAirport"]}'
                            f' → '
                            f'{booking["ToAirport"]}'
                        ),

                    "Travel Date":
                        booking[
                            "DepartureTime"
                        ].strftime("%Y-%m-%d"),

                    "Seat":
                        booking["SeatNumber"],

                    "Class":
                        booking["SeatClass"],

                    "Status":
                        booking[
                            "ReservationStatus"
                        ],

                    "Amount":
                        (
                            f'${float(booking["TotalAmount"]):.2f}'
                        )
                }
            )

        st.dataframe(
            booking_display,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # Active Bookings
        # -------------------------------------------------
        active_bookings = [
            booking
            for booking in bookings
            if booking[
                "ReservationStatus"
            ] != "Cancelled"
        ]

        if active_bookings:

            booking_labels = [
                f'Booking '
                f'#{booking["ReservationID"]} • '
                f'{booking["PassengerName"]} • '
                f'{booking["FlightNumber"]} • '
                f'{booking["DepartureTime"].strftime("%Y-%m-%d")} • '
                f'Seat {booking["SeatNumber"]}'
                for booking in active_bookings
            ]

            selected_booking_label = (
                st.selectbox(
                    "🗂️ Select a booking to cancel",
                    booking_labels
                )
            )

            selected_booking = (
                active_bookings[
                    booking_labels.index(
                        selected_booking_label
                    )
                ]
            )

            # -------------------------------------------------
            # Cancel Reservation
            # -------------------------------------------------
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
                        selected_booking[
                            "ReservationID"
                        ],
                    ))

                    conn.commit()

                    st.success(
                        f"✅ Booking "
                        f"#{selected_booking['ReservationID']} "
                        f"cancelled successfully."
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
        ✈️ <b>SkyTrack</b>
        &nbsp; • &nbsp;
        CS457 Data Modeling and Implementation Techniques
        &nbsp; • &nbsp;
        MySQL + Python + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)