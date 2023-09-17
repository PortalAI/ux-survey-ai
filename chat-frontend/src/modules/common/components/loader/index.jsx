import './index.scss';

const Loader = ({ children, loading }) => (
  <>
    <div className="opaque-loader-wrapper" style={{ display: loading ? 'flex' : 'none' }}>
      <div className="lds-roller">
        <div />
        <div />
        <div />
        <div />
        <div />
        <div />
        <div />
        <div />
      </div>
    </div>
    {children}
  </>
);
export default Loader;
