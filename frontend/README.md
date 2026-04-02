# MediGuide Frontend

Next.js-based web interface for the MediGuide AI medical assistant platform. This frontend provides a user-friendly interface for tourists to access medical assistance services, from symptom reporting to cost estimation.

## 🎯 Features

- **Responsive Design**: Mobile-first UI that works across all devices
- **Authentication**: Integrated Clerk auth for secure user sessions
- **Real-time Updates**: Instant feedback during medical consultations
- **Dark Mode**: Built-in dark theme support
- **Accessible**: WCAG-compliant with Radix UI components
- **Fast**: Optimized Next.js 16 with TypeScript

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- npm, yarn, pnpm, or bun

### Installation

```bash
# Install dependencies
npm install
# or
yarn install
# or
pnpm install
# or
bun install
```

### Configuration

Create a `.env.local` file with:

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development Server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## 📁 Project Structure

```bash
frontend/
├── app/
│   ├── layout.tsx          # Root layout with Clerk auth
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles
├── components/
│   └── ui/                 # Shadcn UI components (Button, etc.)
├── lib/
│   └── utils.ts            # Client-side utilities
├── public/                 # Static assets
├── next.config.ts          # Next.js configuration
├── tailwind.config.ts      # Tailwind CSS configuration
├── tsconfig.json           # TypeScript configuration
└── package.json            # Dependencies
```

## 🛠️ Tech Stack

- **Framework**: Next.js 16.2.2
- **Language**: TypeScript 5
- **UI Components**: Radix UI, Shadcn
- **Styling**: Tailwind CSS 4
- **Authentication**: Clerk
- **Icons**: Lucide React

## 🎨 Available Scripts

| Script          | Purpose                  |
| --------------- | ------------------------ |
| `npm run dev`   | Start development server |
| `npm run build` | Build for production     |
| `npm start`     | Run production server    |
| `npm run lint`  | Run ESLint checks        |

## 🔌 API Integration

The frontend communicates with the FastAPI backend via:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL;

// Example: Making API calls
const response = await fetch(`${API_URL}/health`);
```

Ensure the backend server is running on the configured URL before starting the frontend.

## 🎨 Customization

### Adding Components

Use Shadcn CLI to add components:

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
```

### Styling

- **Global styles**: Edit `app/globals.css`
- **Component styles**: Use Tailwind classes in components
- **Dark mode**: Configured in `tailwind.config.ts`

## 📱 Responsive Design

The application uses Tailwind's responsive utilities:

```tsx
<div className="text-sm sm:text-base md:text-lg lg:text-xl">
  Responsive text
</div>
```

## 🔐 Environment Variables

| Variable                            | Required | Description                         |
| ----------------------------------- | -------- | ----------------------------------- |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Yes      | Clerk public key for authentication |
| `CLERK_SECRET_KEY`                  | Yes      | Clerk secret key for backend        |
| `NEXT_PUBLIC_API_URL`               | Yes      | Backend API URL                     |

## 🚀 Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Other Platforms

The application can be deployed to:

- Netlify
- AWS Amplify
- Docker containers
- Self-hosted servers

Standard Next.js deployment procedures apply.

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Clerk Documentation](https://clerk.com/docs)
- [Shadcn UI](https://ui.shadcn.com)
- [Tailwind CSS](https://tailwindcss.com/docs)

## 🤝 Contributing

See the main [README.md](../README.md) for contribution guidelines.

## 📝 License

Proprietary - All rights reserved.
