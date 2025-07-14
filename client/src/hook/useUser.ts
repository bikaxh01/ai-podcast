import { BASE_URL } from "@/handler/user-apis";
import axios from "axios";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export interface User {
  email: string;
  userName: string;
}

export function useUser(): [User | null, boolean] {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  useEffect(() => {
    const getUser = async () => {
      try {
        setIsLoading(true);
        const res = await axios.get(`${BASE_URL}user/me`, {
          withCredentials: true,
        });

        setUser(res.data.data);
      } catch (err) {
        setUser(null);
        router.push("/auth/sign-in");
      } finally {
        setIsLoading(false);
      }
    };
    getUser();
  }, [router]);

  return [user, isLoading];
}
