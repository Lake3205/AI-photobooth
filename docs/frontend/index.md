# Frontend

The frontend is a Vue 3 application built with TypeScript and Vite. It provides an interactive interface for capturing
photos, analyzing them with AI, and visualizing the results.

## Technology Stack

- **Vue 3** with Composition API
- **TypeScript** for type safety
- **Vite** as build tool
- **Tailwind CSS** for styling
- **Vue Router** for navigation
- **TensorFlow.js** with BlazeFace for face detection
- **Chart.js** for data visualization

## Project Structure

```
frontend/src/
├── pages/          # Route pages (SelfieCamera, Dashboard, Form, Login)
├── components/     # Reusable UI components
├── services/       # API communication and business logic
├── composables/    # Reusable Vue logic (face detection)
├── types/          # TypeScript type definitions
├── router.ts       # Route configuration and guards
└── main.ts         # Application entry point
```

## Key Features

### Photo Capture

Users can capture photos using their webcam or upload existing images. Real-time face detection using TensorFlow.js
provides visual feedback.

### AI Analysis

Uploaded images are sent to the backend where AI models (Gemini, Claude, OpenAI) generate assumptions about the person
in the photo. Results are displayed with confidence indicators.

### Admin Dashboard

Protected admin interface showing aggregated data from all AI analyses. Includes charts and statistics, with the ability
to compare different AI models.

### Survey Form

Token-protected form where users can respond to questions about the AI's assumptions. Access is granted via QR codes or
links after photo capture.

## Routes

- `/` - Main selfie capture page (public)
- `/login` - Admin authentication (public)
- `/dashboard` - Analytics dashboard (admin only)
- `/booth` - Full-screen kiosk mode (admin only)
- `/form` - User survey form (token-protected)
- `/terms-of-service` - Legal information (public)

## Getting Started

### Installation

```bash
cd frontend
npm install
```

### Environment Setup

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

### Development

```bash
npm run dev
```

Runs on `http://localhost:3000`

### Production Build

```bash
npm run build
```

Output in `dist/` directory

## Authentication

The application uses two authentication methods:

1. **JWT Tokens** - For admin routes (dashboard, booth). Tokens are stored in localStorage and validated on each
   navigation.

2. **Form Tokens** - For survey form access. Generated when a photo is analyzed, distributed via QR code or URL
   parameter, stored in cookies.

## Services

Services handle API communication and business logic:

- **authService** - Login, token verification, authentication state
- **webcamService** - Camera access, photo capture, AI analysis
- **formService** - Form data loading and submission
- **dashboardService** - Analytics data fetching and chart generation
- **cookieService** - Cookie management utilities

## Face Detection

The app uses TensorFlow.js with the BlazeFace model for real-time face detection. The model loads automatically when the
camera starts, providing visual feedback to help users position themselves correctly.

## Styling

Uses Tailwind CSS with a dark theme featuring:

- Glassmorphism effects (transparent overlays with backdrop blur)
- Gradient text and backgrounds
- Responsive design (mobile-first approach)
- Smooth transitions and animations

## API Integration

All API calls go through service functions that handle:

- Authentication headers
- Error handling
- Response parsing
- Loading states

Base URL is configured via `VITE_API_URL` environment variable.

## Deployment

The frontend can be deployed using:

- **Docker** - Nginx-based container
- **Static hosting** - Vercel, Netlify, AWS S3, etc.
- **Traditional servers** - Nginx or Apache

See `frontend/Dockerfile` for containerization setup.

## Development Guidelines

- Use TypeScript for all code
- Follow Vue 3 Composition API patterns with `<script setup>`
- Use Tailwind utilities instead of custom CSS
- Keep components focused and single-purpose
- Handle errors gracefully with user feedback
- Ensure mobile responsiveness

