import { Link } from 'react-router-dom'

export default function TermsOfService() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center mb-8">
            <img src="/android-chrome-192x192.png" alt="CalloutRacing Logo" className="h-12 w-12 mr-4" />
            <h1 className="text-3xl font-bold text-gray-900">Terms of Service</h1>
          </div>
          
          <div className="prose prose-lg max-w-none">
            <p className="text-gray-600 mb-6">
              <strong>Last updated:</strong> {new Date().toLocaleDateString()}
            </p>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">1. Acceptance of Terms</h2>
              <p className="text-gray-700 mb-4">
                By accessing and using CalloutRacing ("the Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">2. Description of Service</h2>
              <p className="text-gray-700 mb-4">
                CalloutRacing is a social platform for automotive enthusiasts to connect, organize racing events, share car builds, and engage in the racing community. The Service includes but is not limited to:
              </p>
              <ul className="list-disc pl-6 text-gray-700 mb-4">
                <li>User profiles and social networking features</li>
                <li>Event organization and participation</li>
                <li>Marketplace for automotive parts and services</li>
                <li>Car build documentation and sharing</li>
                <li>Location-based racing spot discovery</li>
                <li>Community forums and messaging</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">3. User Accounts</h2>
              <p className="text-gray-700 mb-4">
                To access certain features of the Service, you must create an account. You are responsible for:
              </p>
              <ul className="list-disc pl-6 text-gray-700 mb-4">
                <li>Maintaining the confidentiality of your account credentials</li>
                <li>All activities that occur under your account</li>
                <li>Providing accurate and complete information</li>
                <li>Updating your account information as necessary</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">4. User Conduct</h2>
              <p className="text-gray-700 mb-4">
                You agree not to use the Service to:
              </p>
              <ul className="list-disc pl-6 text-gray-700 mb-4">
                <li>Violate any applicable laws or regulations</li>
                <li>Harass, abuse, or harm other users</li>
                <li>Post illegal, harmful, or inappropriate content</li>
                <li>Impersonate another person or entity</li>
                <li>Attempt to gain unauthorized access to the Service</li>
                <li>Interfere with the proper functioning of the Service</li>
                <li>Promote illegal racing activities on public roads</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">5. Safety and Legal Compliance</h2>
              <p className="text-gray-700 mb-4">
                Users must comply with all applicable laws and regulations:
              </p>
              <ul className="list-disc pl-6 text-gray-700 mb-4">
                <li>All racing activities must be conducted on private property or designated tracks</li>
                <li>Street racing is strictly prohibited and not condoned by CalloutRacing</li>
                <li>Users are responsible for obtaining necessary permits and insurance</li>
                <li>All vehicles must comply with local safety and emissions regulations</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">6. Content and Intellectual Property</h2>
              <p className="text-gray-700 mb-4">
                You retain ownership of content you post, but grant CalloutRacing a license to use, display, and distribute your content within the Service. You must have the right to share any content you post.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">7. Privacy</h2>
              <p className="text-gray-700 mb-4">
                Your privacy is important to us. Please review our <Link to="/privacy-policy" className="text-red-600 hover:text-red-800 underline">Privacy Policy</Link>, which also governs your use of the Service.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">8. Termination</h2>
              <p className="text-gray-700 mb-4">
                We may terminate or suspend your account at any time for violations of these Terms of Service. You may also terminate your account at any time by contacting us.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">9. Disclaimers</h2>
              <p className="text-gray-700 mb-4">
                The Service is provided "as is" without warranties of any kind. CalloutRacing is not responsible for any injuries, damages, or losses resulting from racing activities or use of the Service.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">10. Limitation of Liability</h2>
              <p className="text-gray-700 mb-4">
                CalloutRacing shall not be liable for any indirect, incidental, special, consequential, or punitive damages resulting from your use of the Service.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">11. Changes to Terms</h2>
              <p className="text-gray-700 mb-4">
                We reserve the right to modify these terms at any time. We will notify users of significant changes via email or through the Service.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">12. Contact Information</h2>
              <p className="text-gray-700 mb-4">
                If you have any questions about these Terms of Service, please contact us at:
              </p>
              <p className="text-gray-700">
                Email: legal@calloutracing.com<br />
                Address: [Your Business Address]
              </p>
            </section>

            <div className="mt-12 pt-8 border-t border-gray-200">
              <Link 
                to="/" 
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Back to Home
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 