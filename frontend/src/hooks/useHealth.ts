import { useEffect, useState } from "react";
import { getHealth } from "../utils/api";

export type HealthState = "checking" | "online" | "offline";

export function useHealth() {
  const [state, setState] = useState<HealthState>("checking");

  useEffect(() => {
    let cancelled = false;

    getHealth()
      .then((response) => {
        if (!cancelled) {
          setState(response.status === "healthy" ? "online" : "offline");
        }
      })
      .catch(() => {
        if (!cancelled) setState("offline");
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return state;
}
