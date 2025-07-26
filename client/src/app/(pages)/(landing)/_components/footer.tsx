import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { MapPin, Linkedin, Twitter, Youtube, Instagram, Rss } from 'lucide-react'; // Using Rss for TikTok placeholder, you can replace it

const footerLinks = [
  {
    title: 'Company',
    links: ['About us', 'Careers', 'For business', 'For media'],
  },
  {
    title: 'Resources',
    links: ['Windows app', 'Playbook', 'Blog', 'Help center'],
  },
  {
    title: 'Community',
    links: ['Events', 'Campus', 'Fellows'],
  },
  {
    title: 'Policy',
    links: ['Terms of service', 'Privacy policy', 'Manage cookies'],
  },
];

const socialLinks = [
  { href: '#', icon: <Linkedin size={20} /> },
  { href: '#', icon: <Twitter size={20} /> },
  { href: '#', icon: <Youtube size={20} /> },
  { href: '#', icon: <Instagram size={20} /> },
  { href: '#', icon: <Rss size={20} /> }, // Placeholder for TikTok
];

function Footer() {
  return (
    <footer className="bg-[#212121] text-gray-400">
      <div className="container mx-auto px-8 py-16">
        <div className="flex flex-col md:flex-row justify-between gap-12">
          {/* Left Section */}
          <div className="flex flex-col gap-4 max-w-sm">
            <Link href="/" className="flex items-center gap-2 mb-2">
              <Image src="/logo.webp" alt="EchoMind Logo" width={32} height={32} />
              <span className="text-white text-2xl font-semibold">EchoMind</span>
            </Link>
            <p className="text-sm">© 2025 EchoMind AI</p>
            <div className="flex items-center gap-2 text-sm">
              <MapPin size={16} />
              <span>108 N Bridge Rd, Singapore</span>
            </div>
            <div className="flex items-center gap-4 mt-4">
              {socialLinks.map((social, index) => (
                <Link key={index} href={social.href} className="hover:text-white transition-colors">
                  {social.icon}
                </Link>
              ))}
            </div>
          </div>

          {/* Right Section - Links */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-8">
            {footerLinks.map((column) => (
              <div key={column.title}>
                <h3 className="font-semibold text-white mb-4">{column.title}</h3>
                <ul className="space-y-3">
                  {column.links.map((link) => (
                    <li key={link}>
                      <Link href="#" className="hover:text-white transition-colors text-sm">
                        {link}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom Slogan */}
        <div className="border-t border-gray-700 mt-16 pt-8 text-center">
          <p className="text-lg italic text-gray-500">
            &#8220; Less talking, more building. &#8221;
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;