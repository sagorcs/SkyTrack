import streamlit as st
from database import get_connection
from datetime import date

# =================================================
# SKYTRACK FLIGHT FARES
# =================================================
FLIGHT_FARES = {
    "ST101": 320.00,
    "ST202": 450.00,
    "ST303": 520.00,
    "ST404": 275.00,
    "ST505": 350.00
}

# =================================================
# PAGE CONFIGURATION
# =================================================
st.set_page_config(
    page_title="SkyTrack",
    page_icon="✈️",
    layout="wide"
)

# =================================================
# PROFESSIONAL COLORFUL UI
# =================================================
st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #eaf4ff 0%, transparent 30%),
        radial-gradient(circle at top right, #f3ecff 0%, transparent 30%),
        linear-gradient(180deg, #f8fbff 0%, #ffffff 52%, #f8fafc 100%);
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(
        120deg,
        #0b1f3a 0%,
        #123b6d 32%,
        #1473b8 68%,
        #5b3cc4 100%
    );

    padding: 42px 46px;
    border-radius: 28px;
    color: white;
    margin-bottom: 25px;

    box-shadow:
        0 18px 45px rgba(30, 64, 175, 0.22);

    position: relative;
    overflow: hidden;
}

.hero::before {
    content: "";
    position: absolute;
    width: 310px;
    height: 310px;
    right: -90px;
    top: -110px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}

.hero::after {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    right: 150px;
    bottom: -120px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}

.hero h1 {
    margin: 0;
    font-size: 52px;
    font-weight: 800;
    position: relative;
    z-index: 2;
}

.hero h3 {
    margin-top: 13px;
    margin-bottom: 8px;
    font-size: 23px;
    font-weight: 500;
    color: #e5efff;
    position: relative;
    z-index: 2;
}

.hero p {
    font-size: 16px;
    color: #dce9ff;
    margin-top: 10px;
    max-width: 850px;
    position: relative;
    z-index: 2;
}

h2 {
    color: #152238;
    font-weight: 750 !important;
    margin-top: 27px !important;
}

div[data-testid="stAlert"] {
    border-radius: 14px;
    border: none;
    box-shadow: 0 5px 16px rgba(15, 23, 42, 0.05);
}

div[data-baseweb="select"] > div {
    border-radius: 12px !important;
    border: 1px solid #d8e1ec !important;
    background-color: white !important;
}

div[data-testid="stDateInput"] input,
div[data-testid="stNumberInput"] input {
    border-radius: 12px !important;
}

div.stButton > button {
    width: 100%;
    border: none;
    border-radius: 13px;
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

    box-shadow:
        0 8px 18px rgba(79, 70, 229, 0.22);
}

div.stButton > button:hover {
    color: white;
    border: none;
    transform: translateY(-1px);

    box-shadow:
        0 12px 24px rgba(79, 70, 229, 0.30);
}

div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #ffffff,
        #f3f8ff
    );

    border: 1px solid #e2e8f0;
    padding: 20px;
    border-radius: 18px;

    box-shadow:
        0 7px 22px rgba(15, 23, 42, 0.07);
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

    box-shadow:
        0 8px 25px rgba(15, 23, 42, 0.07);
}

.summary-card {
    background: linear-gradient(
        135deg,
        #eaf4ff 0%,
        #eef2ff 45%,
        #faf5ff 100%
    );

    border: 1px solid #dbeafe;
    border-radius: 20px;

    padding: 25px;
    margin-top: 18px;
    margin-bottom: 20px;

    box-shadow:
        0 9px 25px rgba(59, 130, 246, 0.10);
}

.summary-title {
    color: #64748b;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 6px;
}

.summary-route {
    color: #1d4ed8;
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 15px;
}

.summary-details {
    color: #334155;
    font-size: 16px;
    line-height: 2;
}

.total-fare-box {
    margin-top: 15px;

    background:
        linear-gradient(
            90deg,
            #dcfce7,
            #ecfdf5
        );

    border: 1px solid #bbf7d0;

    border-radius: 13px;

    padding: 13px 17px;

    color: #047857;

    font-size: 20px;
    font-weight: 800;

    display: inline-block;
}

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

# =================================================
# HERO
# =================================================
st.markdown(
    """
<div class="hero">
<h1>✈️ SkyTrack</h1>
<h3>Airline Reservation & Flight Management System</h3>
<p>
Search flights by destination and travel date, view available seats,
calculate fares automatically, create reservations, and manage bookings
through a MySQL-powered cloud database.
</p>
</div>
""",
    unsafe_allow_html=True
)

# =================================================
# DATABASE CONNECTION TEST
# =================================================
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

# =================================================
# LOAD FLIGHTS
# =================================================
try:

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
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
        """
    )

    flights = cursor.fetchall()

    cursor.close()
    conn.close()

except Exception as e:

    st.error(
        f"Could not load flights: {e}"
    )

    st.stop()

# =================================================
# SEARCH FLIGHT
# =================================================
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

# =================================================
# FILTER FLIGHTS
# =================================================
filtered_flights = [
    flight
    for flight in flights

    if flight["FromAirport"] == from_airport

    and flight["ToAirport"] == to_airport

    and flight["DepartureTime"].date() == travel_date
]

# =================================================
# FLIGHT FOUND
# =================================================
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

                "Departure":
                    flight["DepartureTime"],

                "Arrival":
                    flight["ArrivalTime"],

                "Status":
                    flight["FlightStatus"],

                "Fare / Passenger":
                    f"${fare:.2f}"
            }
        )

    st.dataframe(
        flight_display,
        use_container_width=True,
        hide_index=True
    )

    # =============================================
    # SELECT FLIGHT
    # =============================================
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

    # =============================================
    # FLIGHT SUMMARY
    # =============================================
    st.markdown("## 🌤️ Selected Flight")

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "✈️ Flight",
            selected_flight["FlightNumber"]
        )

    with m2:

        st.metric(
            "🕒 Departure",
            selected_flight[
                "DepartureTime"
            ].strftime("%I:%M %p")
        )

    with m3:

        st.metric(
            "📡 Status",
            selected_flight["FlightStatus"]
        )

    with m4:

        st.metric(
            "💵 Fare / Passenger",
            f"${base_fare:.2f}"
        )

    # =============================================
    # AVAILABLE SEATS
    # =============================================
    st.markdown("## 💺 Available Seats")

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                s.SeatID,
                s.SeatNumber,
                s.SeatClass,
                s.SeatStatus

            FROM Seat s

            WHERE s.FlightID = %s

              AND s.SeatStatus = 'Available'

              AND NOT EXISTS
              (
                    SELECT 1

                    FROM Reservation r

                    WHERE r.SeatID = s.SeatID

                      AND r.FlightID = s.FlightID

                      AND r.ReservationStatus = 'Confirmed'
              )

            ORDER BY s.SeatNumber
            """,
            (
                selected_flight["FlightID"],
            )
        )

        available_seats = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:

        st.error(
            f"Could not load available seats: {e}"
        )

        available_seats = []

    # =============================================
    # RESERVATION AREA
    # =============================================
    if available_seats:

        st.success(
            f"🟢 {len(available_seats)} seat(s) currently available."
        )

        st.dataframe(
            available_seats,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("## 🎫 Make a Reservation")

        # -----------------------------------------
        # Passenger Inputs
        # -----------------------------------------
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
                max_value=min(
                    10,
                    len(available_seats)
                ),
                step=1,
                value=1
            )

        passenger_count = int(passenger_count)

        # -----------------------------------------
        # Seat Options
        # -----------------------------------------
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
            max_selections=passenger_count
        )

        selected_seats = [
            seat_lookup[label]

            for label in selected_seat_labels
        ]

        # -----------------------------------------
        # Fare Calculation
        # -----------------------------------------
        total_amount = (
            base_fare
            *
            passenger_count
        )

        if selected_seats:

            seat_text = ", ".join(
                seat["SeatNumber"]
                for seat in selected_seats
            )

        else:

            seat_text = "Not selected"

        # =========================================
        # FIXED BOOKING SUMMARY
        # =========================================
        summary_html = (
            '<div class="summary-card">'
            '<div class="summary-title">BOOKING SUMMARY</div>'
            '<div class="summary-route">'
            f'{selected_flight["FlightNumber"]} &nbsp; • &nbsp; '
            f'{from_airport} → {to_airport}'
            '</div>'
            '<div class="summary-details">'
            f'📅 <b>Travel Date:</b> '
            f'{travel_date.strftime("%B %d, %Y")}'
            '<br>'
            f'👥 <b>Passengers:</b> '
            f'{passenger_count}'
            '<br>'
            f'💺 <b>Selected Seats:</b> '
            f'{seat_text}'
            '<br>'
            f'💵 <b>Fare:</b> '
            f'${base_fare:.2f} × {passenger_count}'
            '</div>'
            '<div class="total-fare-box">'
            f'Total Fare: ${total_amount:.2f}'
            '</div>'
            '</div>'
        )

        st.markdown(
            summary_html,
            unsafe_allow_html=True
        )

        # =========================================
        # CONFIRM RESERVATION
        # =========================================
        if st.button(
            "✅ Confirm Reservation",
            use_container_width=True
        ):

            if len(selected_seats) != passenger_count:

                st.error(
                    f"Please select exactly "
                    f"{passenger_count} seat(s) "
                    f"for {passenger_count} passenger(s)."
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

                    # ---------------------------------
                    # Validate Passenger ID
                    # ---------------------------------
                    cursor.execute(
                        """
                        SELECT
                            PassengerID,
                            FirstName,
                            LastName

                        FROM Passenger

                        WHERE PassengerID = %s
                        """,
                        (
                            passenger_id,
                        )
                    )

                    passenger = cursor.fetchone()

                    if not passenger:

                        st.error(
                            f"Passenger ID "
                            f"{passenger_id} "
                            f"does not exist."
                        )

                    else:

                        booking_successful = True

                        # -----------------------------
                        # Recheck Seats
                        # -----------------------------
                        for seat in selected_seats:

                            cursor.execute(
                                """
                                SELECT
                                    SeatID,
                                    FlightID,
                                    SeatStatus

                                FROM Seat

                                WHERE SeatID = %s

                                FOR UPDATE
                                """,
                                (
                                    seat["SeatID"],
                                )
                            )

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
                                selected_flight[
                                    "FlightID"
                                ]
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
                                != "Available"
                            ):

                                booking_successful = False

                                st.error(
                                    f'Seat '
                                    f'{seat["SeatNumber"]} '
                                    f'is no longer available.'
                                )

                                break

                            # -------------------------
                            # Active Booking Check
                            # -------------------------
                            cursor.execute(
                                """
                                SELECT ReservationID

                                FROM Reservation

                                WHERE FlightID = %s

                                  AND SeatID = %s

                                  AND ReservationStatus
                                      = 'Confirmed'

                                LIMIT 1
                                """,
                                (
                                    selected_flight[
                                        "FlightID"
                                    ],

                                    seat["SeatID"]
                                )
                            )

                            existing_booking = (
                                cursor.fetchone()
                            )

                            if existing_booking:

                                booking_successful = False

                                st.error(
                                    f'Seat '
                                    f'{seat["SeatNumber"]} '
                                    f'is already booked.'
                                )

                                break

                        # -----------------------------
                        # Insert Reservations
                        # -----------------------------
                        if booking_successful:

                            for seat in selected_seats:

                                cursor.execute(
                                    """
                                    INSERT INTO Reservation
                                    (
                                        PassengerID,
                                        FlightID,
                                        SeatID,
                                        ReservationStatus,
                                        TotalAmount
                                    )

                                    VALUES
                                    (
                                        %s,
                                        %s,
                                        %s,
                                        'Confirmed',
                                        %s
                                    )
                                    """,
                                    (
                                        passenger_id,

                                        selected_flight[
                                            "FlightID"
                                        ],

                                        seat["SeatID"],

                                        base_fare
                                    )
                                )

                            conn.commit()

                            st.success(
                                f"🎉 Reservation confirmed for "
                                f"{passenger_count} passenger(s)! "
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

# =================================================
# NO FLIGHT
# =================================================
else:

    st.warning(
        f"⚠️ No flights available from "
        f"{from_airport} to {to_airport} "
        f"on "
        f"{travel_date.strftime('%B %d, %Y')}."
    )

# =================================================
# MANAGE BOOKINGS
# =================================================
st.divider()

st.markdown("## 📋 Manage Bookings")

try:

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
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
            ON f.DepartureAirportID
            = da.AirportID

        JOIN Airport aa
            ON f.ArrivalAirportID
            = aa.AirportID

        JOIN Seat s
            ON r.SeatID = s.SeatID

        ORDER BY r.ReservationID DESC
        """
    )

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
                        ].strftime(
                            "%Y-%m-%d"
                        ),

                    "Seat":
                        booking["SeatNumber"],

                    "Class":
                        booking["SeatClass"],

                    "Status":
                        booking[
                            "ReservationStatus"
                        ],

                    "Amount":
                        f'${float(booking["TotalAmount"]):.2f}'
                }
            )

        st.dataframe(
            booking_display,
            use_container_width=True,
            hide_index=True
        )

        # =============================================
        # ACTIVE BOOKINGS
        # =============================================
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

            selected_booking_label = st.selectbox(
                "🗂️ Select a booking to cancel",
                booking_labels
            )

            selected_booking = (
                active_bookings[
                    booking_labels.index(
                        selected_booking_label
                    )
                ]
            )

            # =========================================
            # CANCEL
            # =========================================
            if st.button(
                "❌ Cancel Reservation",
                use_container_width=True
            ):

                conn = None
                cursor = None

                try:

                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        UPDATE Reservation

                        SET ReservationStatus
                            = 'Cancelled'

                        WHERE ReservationID = %s

                          AND ReservationStatus
                              != 'Cancelled'
                        """,
                        (
                            selected_booking[
                                "ReservationID"
                            ],
                        )
                    )

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

# =================================================
# FOOTER
# =================================================
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