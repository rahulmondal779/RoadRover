# RoadRover Rental Car Management System

RoadRover is a rental car management system designed to simplify the process of renting cars for both customers and administrators. This system allows users to browse available cars, make reservations, apply coupons, and manage their bookings efficiently.

## Features

- **User Authentication**: Secure user authentication system for customers and administrators.
- **Car Listings**: Browse available cars with details such as model, brand, price, and availability.
- **Reservation Management**: Users can reserve cars for specific dates and times.
- **Coupon System**: Apply discount coupons during the booking process to avail discounts.
- **User Profile**: View and manage user profiles with booking history and preferences.
- **Admin Dashboard**: Administrators have access to an admin dashboard to manage cars, bookings, and users.
- **Responsive Design**: The system is designed with responsiveness in mind, ensuring usability across various devices.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Python, Django
- **Database**: SQLite (for development)
- **Other Tools**: Git, GitHub, Heroku (for deployment)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/rahulmondal779/RoadRover.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start the development server:

```bash
python manage.py runserver
```

5. Open your web browser and navigate to `http://localhost:8000` to view the application.

## Usage

- Visit the website and sign up as a new user or log in with existing credentials.
- Browse available cars, make reservations, and apply coupons during the booking process.
- Administrators can log in to the admin dashboard (`/admin`) to manage cars, bookings, and users.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.1/getting-started/introduction/)
- [Font Awesome](https://fontawesome.com/)
- [Unsplash](https://unsplash.com/) (for placeholder images)
