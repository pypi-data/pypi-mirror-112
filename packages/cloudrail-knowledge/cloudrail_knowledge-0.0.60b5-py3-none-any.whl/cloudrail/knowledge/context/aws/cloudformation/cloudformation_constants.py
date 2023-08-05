from enum import Enum


class CloudformationResourceType(str, Enum):
    VPC = 'AWS::EC2::VPC'
    EC2_INSTANCE = 'AWS::EC2::Instance'
    SUBNET = 'AWS::EC2::Subnet'
    SECURITY_GROUP = 'AWS::EC2::SecurityGroup'
    S3_BUCKET = 'AWS::S3::Bucket'
