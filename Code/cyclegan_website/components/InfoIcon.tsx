interface InfoIconProps {
  fill?: string;
  size?: number;
  height?: number;
  width?: number;
}

export const InfoIcon = ({
  fill = "currentColor",
  size = undefined,
  height = undefined,
  width = undefined,
  ...props
}: InfoIconProps) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size || width || 24}
      height={size || height || 24}
      viewBox="0 0 24 24"
      {...props}
    >
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M7.66988 1.99921H16.3399C19.7299 1.99921 21.9999 4.37921 21.9999 7.91921V16.0902C21.9999 19.6202 19.7299 21.9992 16.3399 21.9992H7.66988C4.27988 21.9992 1.99988 19.6202 1.99988 16.0902V7.91921C1.99988 4.37921 4.27988 1.99921 7.66988 1.99921ZM11.9899 9.06021C11.5199 9.06021 11.1299 8.66921 11.1299 8.19021C11.1299 7.70021 11.5199 7.31021 12.0099 7.31021C12.4899 7.31021 12.8799 7.70021 12.8799 8.19021C12.8799 8.66921 12.4899 9.06021 11.9899 9.06021ZM12.8699 15.7802C12.8699 16.2602 12.4799 16.6502 11.9899 16.6502C11.5099 16.6502 11.1199 16.2602 11.1199 15.7802V11.3602C11.1199 10.8792 11.5099 10.4802 11.9899 10.4802C12.4799 10.4802 12.8699 10.8792 12.8699 11.3602V15.7802Z"
        fill={fill}
      />
    </svg>
  );
};
