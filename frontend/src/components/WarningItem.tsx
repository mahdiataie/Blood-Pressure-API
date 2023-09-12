import { Alert } from 'antd';
import moment from 'moment';
import { FC } from 'react';


export interface IWarningItem {
    warning_code: 'RED' | 'YELLOW' | 'GREEN',
    value: Float32Array,
    timestamp: string,
    uuid: string,
    measuretype_name: string,
    deviceID?: string,
}

export interface WarningItemProps {
    warning: IWarningItem
}

const WarningItem: FC<WarningItemProps> = ({ warning }) => {
    const { warning_code, value, timestamp, measuretype_name } = warning;
    let formattedDate = (moment(timestamp)).format('DD-MMM-YYYY LT')

    return (
        <>
            {<Alert
                message={measuretype_name}
                description={
                    <>
                        <p>timestamp: {formattedDate}</p>
                        <p>Value: {value}</p>
                    </>}
                type={warning_code === 'YELLOW' ? "warning" : "error"}
            />}
        </>
    );
}

export default WarningItem;