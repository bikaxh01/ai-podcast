import { validateUserEmail } from "@/handler/user-apis";

export type EmailValidationMessage = {
  success: boolean;
  message: string;
};

export async function ValidateEmail(
  email: string
): Promise<EmailValidationMessage> {
  const validateEmailRegex = /^\S+@\S+\.\S+$/;
  const isValid = validateEmailRegex.test(email);
  if (!isValid) {
    return { success: false, message: "Invalid email format" };
  }

  // api call check
  const res = await validateUserEmail(email);
  return res;
}
