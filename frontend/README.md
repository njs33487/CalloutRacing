# CalloutRacing Frontend

A React-based frontend for the CalloutRacing drag racing social network.

## Features

- **Authentication**: Login, signup, and logout functionality
- **Protected Routes**: Secure access to authenticated pages
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **API Integration**: Full integration with Django REST API
- **Modern UI**: Professional design with red, white, and yellow color scheme

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
# Copy the example environment file
cp env.example .env
```

3. Update the `.env` file with your API URL:
```
VITE_API_URL=https://calloutracing.up.railway.app/api
```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Building for Production

Build the application:
```bash
npm run build
```

The built files will be in the `dist/` directory.

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── Layout.tsx      # Main layout with navigation
│   └── ProtectedRoute.tsx # Authentication guard
├── contexts/           # React contexts
│   └── AuthContext.tsx # Authentication state management
├── pages/              # Page components
│   ├── About.tsx       # Landing page
│   ├── Login.tsx       # Login form
│   ├── Signup.tsx      # Registration form
│   ├── Contact.tsx     # Contact form
│   ├── Home.tsx        # Dashboard
│   ├── Callouts.tsx    # Callouts list
│   ├── Events.tsx      # Events list
│   ├── Marketplace.tsx # Marketplace
│   └── Profile.tsx     # User profile
├── services/           # API services
│   └── api.ts         # API client and endpoints
├── App.tsx            # Main app component
└── main.tsx           # Entry point
```

## Authentication

The application uses token-based authentication:

1. **Login**: Users can log in with username and password
2. **Registration**: New users can create accounts
3. **Protected Routes**: Authenticated users can access the app dashboard
4. **Logout**: Users can log out and clear their session

## API Integration

The frontend connects to the Django REST API with the following features:

- **Automatic Token Management**: Tokens are stored in localStorage
- **Request Interceptors**: Automatically adds auth headers to requests
- **Error Handling**: Handles API errors and authentication failures
- **Response Interceptors**: Redirects to login on 401 errors

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Environment Variables

- `VITE_API_URL` - Backend API URL (default: https://calloutracing.up.railway.app/api)
- `VITE_APP_NAME` - Application name
- `VITE_DEV_MODE` - Development mode flag

## Styling

The application uses:
- **Tailwind CSS** for styling
- **Heroicons** for icons
- **Custom color scheme**: Red, white, and yellow theme

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Deployment

The frontend can be deployed to any static hosting service:

1. Build the application: `npm run build`
2. Upload the `dist/` folder to your hosting provider
3. Configure environment variables for production

For Railway deployment, the application is configured to build and serve automatically. 