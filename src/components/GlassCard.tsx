import React from "react";
import { View, ViewProps } from "react-native";

export const GlassCard: React.FC<ViewProps> = ({ children, className, ...props }) => {
  return (
    <View 
      className={`bg-white/10 border border-white/20 rounded-2xl overflow-hidden ${className}`}
      style={{
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 5,
      }}
      {...props}
    >
      <View className="p-4 bg-white/5">
        {children}
      </View>
    </View>
  );
};
