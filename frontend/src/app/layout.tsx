export const metadata = {
  title: 'Dashboard Educativo',
  description: 'Sistema de gestión educativa',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body>
        {children}
      </body>
    </html>
  );
}