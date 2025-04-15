# OurChants-Backend Frontend Specification

## Overview

Create a modern, responsive web application for managing song data that integrates with the OurChants-Backend API. The application should provide a user-friendly interface for viewing, creating, editing, and deleting song information.

## Technical Stack

- **Framework**: React.js with TypeScript
- **State Management**: Redux Toolkit
- **Styling**: Tailwind CSS
- **API Client**: Axios
- **Form Handling**: React Hook Form with Zod validation
- **Testing**: Jest and React Testing Library
- **Build Tool**: Vite

## Core Features

### 1. Song Management

#### Song List View
- Display songs in a responsive grid/list
- Sortable columns (name, artist, album, release date, genre)
- Search functionality across all fields
- Pagination (20 items per page)
- Filter by genre
- Responsive design (mobile-first)

#### Song Detail View
- Display all song information
- Show album art (if available)
- Edit/Delete actions
- Back to list navigation

#### Song Creation/Edit Form
- Form validation for all fields
- Date picker for release date
- Duration input in minutes:seconds format
- Genre selection from predefined list
- Image upload for album art
- Cancel/Save actions

### 2. User Interface Components

#### Layout
- Header with navigation
- Main content area
- Footer with version info
- Loading states
- Error boundaries

#### Common Components
- SearchBar
- SortableTable
- Pagination
- Modal (for delete confirmation)
- Toast notifications
- Loading spinner
- Error message

### 3. State Management

#### Redux Store Structure
```typescript
interface Song {
  id: string;
  name: string;
  artist: string;
  album: string;
  release_date: string;
  genre: string;
  duration_in_seconds: number;
  description?: string;
}

interface AppState {
  songs: {
    items: Song[];
    loading: boolean;
    error: string | null;
    pagination: {
      currentPage: number;
      totalPages: number;
      itemsPerPage: number;
    };
    filters: {
      search: string;
      genre: string;
      sortBy: string;
      sortOrder: 'asc' | 'desc';
    };
  };
}
```

### 4. API Integration

#### Endpoints
```typescript
const API_ENDPOINTS = {
  GET_SONGS: '/songs',
  GET_SONG: (id: string) => `/songs/${id}`,
  CREATE_SONG: '/songs',
  UPDATE_SONG: (id: string) => `/songs/${id}`,
  DELETE_SONG: (id: string) => `/songs/${id}`,
};
```

#### API Client Configuration
- Base URL from environment variable
- Error handling middleware
- Request/Response interceptors
- Authentication headers (if needed)

### 5. Form Validation

```typescript
const songSchema = z.object({
  name: z.string().min(1, "Name is required"),
  artist: z.string().min(1, "Artist is required"),
  album: z.string().min(1, "Album is required"),
  release_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Invalid date format"),
  genre: z.string().min(1, "Genre is required"),
  duration_in_seconds: z.number().min(1, "Duration must be positive"),
  description: z.string().optional(),
});
```

### 6. Styling Guidelines

#### Color Palette
```typescript
const colors = {
  primary: '#3B82F6',    // Blue
  secondary: '#10B981',  // Green
  danger: '#EF4444',     // Red
  warning: '#F59E0B',    // Yellow
  background: '#F3F4F6', // Light gray
  text: '#1F2937',       // Dark gray
};
```

#### Typography
- Font family: Inter
- Base size: 16px
- Headings: 24px, 20px, 18px
- Body text: 16px
- Small text: 14px

#### Spacing
- Base unit: 4px
- Container padding: 24px
- Component spacing: 16px
- Form field spacing: 12px

### 7. Responsive Design

#### Breakpoints
```typescript
const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
};
```

#### Layout Variations
- Mobile: Single column
- Tablet: Two columns
- Desktop: Three columns
- Large desktop: Four columns

### 8. Error Handling

- Network error messages
- Form validation errors
- API error messages
- 404 page
- Error boundary for React errors

### 9. Performance Considerations

- Lazy loading for routes
- Image optimization
- Memoization for expensive computations
- Virtualized list for large datasets
- Code splitting

### 10. Testing Requirements

#### Unit Tests
- Component rendering
- Redux actions/reducers
- Form validation
- Utility functions

#### Integration Tests
- API integration
- Form submission
- Navigation flow

#### Accessibility Tests
- Keyboard navigation
- Screen reader compatibility
- Color contrast
- ARIA labels

### 11. Development Guidelines

#### Code Structure
```
src/
├── components/
│   ├── common/
│   ├── layout/
│   └── songs/
├── features/
│   └── songs/
├── services/
│   └── api/
├── store/
│   ├── slices/
│   └── hooks/
├── utils/
├── types/
└── styles/
```

#### Naming Conventions
- Components: PascalCase
- Files: kebab-case
- Variables: camelCase
- Constants: UPPER_SNAKE_CASE
- Types/Interfaces: PascalCase with 'I' prefix

### 12. Build and Deployment

#### Environment Variables
```typescript
interface Env {
  VITE_API_URL: string;
  VITE_ENV: 'development' | 'production';
  VITE_VERSION: string;
}
```

#### Build Scripts
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "test": "jest",
    "lint": "eslint src --ext ts,tsx",
    "format": "prettier --write src"
  }
}
```

### 13. Documentation Requirements

- Component documentation
- API integration guide
- State management documentation
- Setup instructions
- Contribution guidelines

### 14. Future Considerations

- User authentication
- Favorites system
- Playlist creation
- Audio preview
- Social sharing
- Analytics integration 