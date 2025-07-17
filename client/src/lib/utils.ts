import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { formatDistanceToNow } from "date-fns";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDateTime(isoString: string): string {
  const date = new Date(isoString);
  
  // Options for formatting
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  };
  
  return date.toLocaleDateString('en-US', options).replace(/,/g, ' -');
}

export function formatDistanceToNowCustom(isoString: string): string {
  const date = new Date(isoString);
  return formatDistanceToNow(date, { addSuffix: true });
}